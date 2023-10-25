options(warn=-1)

library(ggplot2)
                             
default_colors <- scale_color_discrete()$palette(2)
legend_title <- '{legend_title}'

data <- read.csv('processed_stats.tsv', sep='\t', check.names=F)

p <- ggplot(data, aes(x=as.factor(share_count), y=mean, fill=share_type)) +
     geom_boxplot(
        aes(ymin=min, lower=p25, middle=p50, upper=p75, ymax=max),
        stat='identity',
        position='identity'
    ) + 
    geom_smooth(aes(y=mean, group=share_type, color=share_type), method='auto', span=1, se=F) +
    labs(x='Genomes', y='Families', title='BoxPlot') +
    theme_bw() + 
    theme(
        panel.border=element_blank(),
        panel.grid.major=element_blank(),
        panel.grid.minor=element_blank(),
        axis.line=element_line(colour='black')
    ) +
    scale_color_manual(name=legend_title, values=default_colors) +
    scale_fill_manual(name=legend_title, values=default_colors)
                   

ggsave(filename='boxplot.png', plot=p, dpi=300, type='cairo', width=14, height=7)
cat('\x1b[32msaved png file to: boxplot.png\x1b[0m\n')

ggsave(filename='boxplot.pdf', plot=p, dpi=300, width=14, height=7)
cat('\x1b[32msaved pdf file to: boxplot.pdf\x1b[0m\n')
