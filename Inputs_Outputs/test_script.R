mydata <- read.table("img58_6.txt", header = TRUE, sep = " ", dec = ".")

plot(mydata[[1]], mydata[[3]], main="Taux de recouvrement et nombre d'occurrence pour des motifs de 6 sommets - img58", xlab="Motifs à isomorphisme près", ylab="Nombre d'occurrence", pch=20, col="blue")
text(mydata[[1]], mydata[[3]], labels=mydata[[2]], cex=labels.size, pos=labels.position)
