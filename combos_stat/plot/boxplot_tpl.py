import string

R_CODE_TPL = string.Template('''\
options(warn=-1)

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
cat('\\x1b[32msaved png file to: ${output}.png\\x1b[0m\\n')

ggsave(filename='${output}.pdf', plot=p, dpi=${dpi}, width=${width}, height=${height})
cat('\\x1b[32msaved pdf file to: ${output}.pdf\\x1b[0m\\n')
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
    """
    Generate R code to create a boxplot visualization using ggplot2.

    This function produces R code based on the provided parameters to read a preprocessed data file,
    generate a boxplot, and save the resulting visualization as both a PNG and PDF file.

    Parameters:
    - infile (str, optional): Path to the input CSV file containing preprocessed data. Default is 'processed_stats.tsv'.
    - output (str, optional): Prefix for the output image filenames. Default is 'boxplot'.
    - x_lab (str, optional): Label for the x-axis. Default is 'Genomes'.
    - y_lab (str, optional): Label for the y-axis. Default is 'Families'.
    - title (str, optional): Title for the plot. Default is 'BoxPlot'.
    - dpi (int, optional): Resolution for the saved images. Default is 300.
    - width (int, optional): Width of the saved images in inches. Default is 14.
    - height (int, optional): Height of the saved images in inches. Default is 7.
    - **kwargs: Additional keyword arguments.

    Returns:
    - str: Generated R code.
    """
    script = R_CODE_TPL.substitute(**locals())
    return script
