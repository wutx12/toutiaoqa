# install.packages("devtools")
# follow "http://www.libfm.org/libfm-1.42.manual.pdf" to compile libFM
rm(list=ls(all=TRUE))
devtools::install_github("andland/libFMexe")

library(libFMexe)

cwd = dirname(sys.frame(1)$ofile)
dataPath = paste0(cwd, "/../../../data/")
df <- read.table(paste0(dataPath, "invited_info_train.txt"), header = FALSE) 
colnames(df) <- c("questionId", "userId", "ansOrNot")

validation <- read.csv(paste0(dataPath, "validate_nolabel.txt"), header = TRUE) 
colnames(validation) <- c("questionId", "userId", "ansOrNot")
validation$ansOrNot <- rep(1, nrow(validation))

set.seed(123)
train_rows = sample.int(nrow(df), nrow(df) * 2 / 3)
train = df[train_rows, ]
test  = df[-train_rows, ]

# function to find optimal threshold for classifier
# install.packages("ROCR")
library(ROCR)
optimalThres <- function(predScale, trueLab, candThresList) {
  bestF1 = -1
  bestCand = 0
  for (thres in candThresList) {
    predLab <- (predScale > thres) + 0
    pred <- prediction(predLab, trueLab)
    predTrueN = length(which(predLab > 0))
    realTrueN = length(which(trueLab > 0))
    predRightN = length(which(predLab > 0 & trueLab > 0))
    fScore = 2 * predRightN /(predTrueN + realTrueN)
    if (fScore > bestCand) {
      bestCand = thres
      bestF1 = fScore
    }
  }
  return(bestCand)
}

# train FM using questionId and userId only
predFM = libFM(train=df, test=validation, formula=ansOrNot ~ questionId + userId, validation = test, task = "c", 
               dim = 10, iter = 500, 
               exe_loc = paste0(cwd, "/../../lib/libfm-1.42/bin"))
comp <- cbind(validation, predFM)
#comp <- comp[order(-comp$predFM), ]
#comp <- comp[order(comp$questionId), ]

# valid_row = sample.int(nrow(comp), nrow(comp) * 1 / 4)
# valid = comp[valid_row, ]
# metric = comp[-valid_row, ]

# install.packages("rPython)

predLab = (comp$predFM > 0.5) + 0
out <- cbind(comp$questionId, comp$userId, predLab)
colnames(out)<- c("qid","uid","label")
write.table(out,"/Users/xinghai/Documents/learning/toutiao/toutiaoqa/data/out.csv", row.names=FALSE, quote=FALSE)


library(rPython)
python.load(paste0(cwd, "/", "ndcg.py"))

