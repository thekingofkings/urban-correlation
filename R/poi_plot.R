library(maptools)
library(gplots)
library(grDevices)


NTAs <- readShapeSpatial("../../../dataset/nynta_14c/wgs84")

NTAs <- subset(NTAs, substr(NTACode, 0, 2) == "MN")
cr <- coordinates(NTAs)


ids <- as.character(NTAs$NTACode)




pois <- read.csv("../data/nta_poi.csv")
pois <- pois[,ids]

chooseColor <- colorRampPalette( c('white', 'darkgreen') )

for (i in 1:10) {
    pdf(file=paste("poi-",i,".pdf", sep=""), width=7, height=7)
    par(mai=c(0,0,0,0))
    plot(NTAs, border='blue', col=chooseColor(50)[findInterval( pois[i,],
                                  seq(0, max(pois[i,]), max(pois[i,])/49))])
    text(cr, labels=ids)
    dev.off()
}
