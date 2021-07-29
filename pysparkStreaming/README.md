The structured streaming with pyspark application takes the number of tweets that 
one wants to stream and the hashtag they're interested in and ouputs counts
the number of related hashtags in the same tweet through pyspark's structured streaming API.
A graph is outputed every two seconds which is also the trigger at which pyspark produces the next
table in memory. The final result is also displayed when the number of tweets read have reached the limit.
