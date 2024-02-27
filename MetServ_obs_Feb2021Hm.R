#####################################################################
#                                                                   #
# Program to extract MetService data from observation archive       #
# for use in validation of WRF output data                          #
# Written/updated by Andy Sturman February 2021                     #
#                                                                   #
#####################################################################
#
# require(data.table)
# require(xts)
library(plyr)
library(dplyr)
library(data.table)
#
# Set working directory path
setwd("F:/Working_folder/Current_wineclimate/WRF_model_2020/validation")
#
# Set path to data
#
path <- "F:/Research/Wine climate/SLMACC project/Current_work/Data analysis/MetService data/"
#
# Read in year required
#
  year <- fread("year.txt")
#
# Read in months (two digits)
#
  months <- as.character(c('01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12'))
  ndays <- as.character(c('31', '28', '31', '30', '31', '30', '31', '31', '30', '31', '30', '31'))
#
# Check for leap year
#  
 if((year %% 4) == 0) {ndays <- as.character(c('31', '29', '31', '30', '31', '30', '31', '31', '30', '31', '30', '31'))
 }
# Read in list of site names
#
AWS <- read.csv("AWS.txt", header = FALSE)
colnames(AWS) <- c("Location", "Site_name")
# 
# Set number of sites
#
  n = 3
#
# Start month loop (01 to 12)
#
for (i in 1:12){
  month <- months[i]
#
# Start day loop 
#
  for (j in 1:ndays[i]){
  #
  # Read in met data file 1
  #
    if (j<10) {day <- paste("0",j, sep = "")}
    else {day <- j}
    #
    # Read in met data file 1
    #
    filename <- paste("obs_AM_",year,month,day,"0030.csv", sep = "")
    f <- file.path(path, filename)
    if (file.exists(f)){
      data1 <- fread(f,sep=',')
      data1 <- data.table(data1)}
    #
    # Read in met data file 2
    #
    filename <- paste("obs_NZ_",year,month,day,"0030.csv", sep = "")
    f <- file.path(path, filename)
    if (file.exists(f)){
      data2 <- fread(f,sep=',')
      data2 <- data.table(data2)}
#
# Subset data columns required
# Location,DateTime(UTC),Wind Dir,Wind Spd(kt),Max Gust(kt),Temp,Dew Point,RH,Rainfall(mm),Pressure,Cloud
#
  data1 <- subset(data1, select = c(1,2,3,4,5,6,7,8,9,10))
  data2 <- subset(data2, select = c(1,2,3,4,5,6,7,8,9,10))
#
#
# Extract data from each data file for each AWS station
#
# This loop selects each station location sequentially
#

for (i in 1:n){
  newdata1 <- select(filter(data1, Location == toString(AWS[i,1])),c(1,2,3,4,5,6,7,8,9,10))
  # print(newdata1)
  write.table(newdata1, AWS[i,1], sep=",", col.names = F, row.names = F, append=TRUE)
}

for (i in 1:n){
  newdata2 <- select(filter(data2, Location == toString(AWS[i,1])),c(1,2,3,4,5,6,7,8,9,10))
  # print(newdata2)
  write.table(newdata2, AWS[i,1], sep=",", col.names = F, row.names = F, append=TRUE)
}

  # End of day loop

}
  
  # End of month loop
  
}  
  
  
