# Run from R Console: setwd('/Users/Sal/Desktop')
# source('input.r')

# Install packages stringr stringi s
library(stringr)
require(stringr)


# autoParse parses the content of a webpage and saves the text portion in a folder
# the autoParse code is reused. It is extracted from 
# https://data.world/jumpyaf/2013-2016-cleaned-parsed-10-k-filings-with-the-sec/workspace/file?filename=Algorithm.md
# with the original author being Eric He
autoParse <- function(url,i)
{
  readLines(url, encoding = "UTF-8") %>% 
  str_c(collapse = " ") %>% 
  str_extract(pattern = "(?s)(?m)<TYPE>10-K.*?(</TEXT>)") %>%
  str_replace(pattern = "((?i)<TYPE>).*?(?=<)", replacement = "") %>% 
  str_replace(pattern = "((?i)<SEQUENCE>).*?(?=<)", replacement = "") %>%  
  str_replace(pattern = "((?i)<FILENAME>).*?(?=<)", replacement = "") %>%
  str_replace(pattern = "((?i)<DESCRIPTION>).*?(?=<)", replacement = "") %>%
  str_replace(pattern = "(?s)(?i)<head>.*?</head>", replacement = "") %>%
  str_replace(pattern = "(?s)(?i)<(table).*?(</table>)", replacement = "") %>%
  str_replace_all(pattern = "(?s)(?i)(?m)> +Item|>Item|^Item", replacement = ">°Item") %>%  
  str_replace_all(pattern = "(?s)<.*?>", replacement = " ") %>%  
  str_replace_all(pattern = "&(.{2,6});", replacement = " ") %>%  
  str_replace_all(pattern = "(?s) +", replacement = " ") %>%  
  write(file = paste(output, toString(i), '.txt', sep = ""))
}


  input <- "C:/Users/josh/Desktop/scrape"
  output <- "E:/"
  my_data <- read.csv("C:/Users/josh/Desktop/scrape/firm.csv")

  adsh=my_data[['adsh']]
  cik=my_data[['cik']]
  len=length(adsh)
  min=(len+1)/2
  # creating datatable for faster access
  # dt=data.table(a=adsh,b=cik)

  # This for loop loops throught he csv file, extracting each adsh number to form urls for 
  # autoParse to parse. 
  

  for (i in 21299:len)
  {
  	unsplit_adsh=adsh[i]
    split_adsh <- strsplit(toString(unsplit_adsh),"-")[[1]]
    unhyphened_adsh=paste(split_adsh[1], split_adsh[2], split_adsh[3],
      sep="", collapse=NULL) 
    cik_num=toString(cik[i])
    url=paste('https://www.sec.gov/Archives/edgar/data/',
      cik_num, '/', unhyphened_adsh, '/', unsplit_adsh,'.txt', sep="", collapse=NULL)
    print(url)
    autoParse(url,i)
  }


