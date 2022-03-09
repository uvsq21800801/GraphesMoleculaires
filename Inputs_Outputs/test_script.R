mydata <- read.table("img58_6.txt", header = TRUE, sep = " ", dec = ".")

plot(mydata[[1]], mydata[[3]], main="Taux de recouvrement par nombre d'occurance croissant pour des sous-graphe d'ordre 6 - img58", xlab="Groupes de sous-graphes à isomorphisme près", ylab="Nombre d'occurance", pch=20, col="blue")
text(mydata[[1]], mydata[[3]], labels=mydata[[2]], cex=labels.size, pos=labels.position)
