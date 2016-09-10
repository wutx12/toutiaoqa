# install.packages("devtools")
# follow "http://www.libfm.org/libfm-1.42.manual.pdf" to compile libFM
rm(list=ls(all=TRUE))
devtools::install_github("andland/libFMexe")

library(libFMexe)

cwd = dirname(sys.frame(1)$ofile)
dataPath = paste0(cwd, "/../../data/")
df <- read.table(paste0(dataPath, "invited_info_train.txt"), header = FALSE) 
colnames(df) <- c("questionId", "userId", "ansOrNot")

set.seed(123)
train_rows = sample.int(nrow(df), nrow(df) * 2 / 3)
train = df[train_rows, ]
test  = df[-train_rows, ]

predFM = libFM(train, test, ansOrNot ~ questionId + userId, task = "c", dim = 10, iter = 500, exe_loc = "/Users/xinghai/Documents/learning/toutiao/toutiaoqa/TouTiaoQA/lib/libfm-1.42/bin")
comp <- cbind(test, predFM)
comp <- comp[order(-comp$predFM), ]
comp <- comp[order(comp$questionId), ]