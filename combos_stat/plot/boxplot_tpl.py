import string

R_CODE_TPL = string.Template('''\
library(ggplot2)

# 读取预处理后的数据
data <- read.csv('${infile}', sep='\\t', check.names=F)

# 绘制箱线图
p <- ggplot(data, aes(x=as.factor(share_count), y=mean, fill=share_type)) +
     geom_boxplot(
        aes(ymin=min, lower=p25, middle=p50, upper=p75, ymax=max),
        stat='identity'
    ) + 
    geom_smooth(aes(y=mean, group=share_type, color=share_type), method='auto', span=1, se=F) + # 添加平滑曲线
    labs(x='${x_lab}', y='${y_lab}', title='${title}') +
    theme_bw() + 
    theme(
        panel.border=element_blank(),
        panel.grid.major=element_blank(),
        panel.grid.minor=element_blank(),
        axis.line=element_line(colour ='black')
    )

# 保存图片
ggsave(filename='${output}.png', plot=p, dpi=${dpi}, type='cairo', width=${width}, height=${height})
ggsave(filename='${output}.pdf', plot=p, dpi=${dpi}, width=${width}, height=${height})
''')


def generate_r_code(infile='processed_stats.tsv',
                    output='boxplot',
                    x_lab='Genomes',
                    y_lab='Families',
                    title='BoxPlot',
                    dpi=300,
                    width=14,
                    height=7,
                    **kwargs):
    script = R_CODE_TPL.substitute(**locals())
    return script
