import string

R_CODE_TPL = string.Template('''\
options(warn=-1)

library(ggplot2)
                             
default_colors <- scale_color_discrete()$$palette(2)
legend_title <- '${legend_title}'

data <- read.csv('${infile}', sep='\\t', check.names=F)

p <- ggplot(data, aes(x=as.factor(share_count), y=value, color=share_type, shape=share_type)) +
    geom_point(alpha=0.6, size=3) +  # 设置点的透明度和大小                     
    scale_shape_manual(
        values=c(16, 17)    # 实心：16是圆形，17是三角形
        # values=c(1, 2)      # 空心：1是圆形，2是三角形
    ) + 
    geom_smooth(
        aes(y=value, group=share_type, color=share_type),
        method='loess',
        span=1,
        se=F
    ) + # 添加平滑曲线，se为置信区间
    labs(x='${x_lab}', y='${y_lab}', title='${title}') +
    theme_bw() + 
    theme(
        panel.border=element_blank(),
        panel.grid.major=element_blank(),
        panel.grid.minor=element_blank(),
        axis.line=element_line(colour='black')
    ) +
    scale_color_manual(name=legend_title, values=default_colors) +
    scale_fill_manual(name=legend_title, values=default_colors)

ggsave(filename='${output}.png', plot=p, dpi=${dpi}, type='cairo', width=${width}, height=${height})
cat('\\x1b[32msaved png file to: ${output}.png\\x1b[0m\\n')

ggsave(filename='${output}.pdf', plot=p, dpi=${dpi}, width=${width}, height=${height})
cat('\\x1b[32msaved pdf file to: ${output}.pdf\\x1b[0m\\n')
''')


def generate_r_code(infile='processed_stats.tsv',
                    output='pointplot',
                    x_lab='Genomes',
                    y_lab='Families',
                    title='',
                    legend_title='Type',
                    dpi=300,
                    width=14,
                    height=7,
                    **kwargs):
    """
    Generate R code to create a pointplot visualization using ggplot2.

    This function produces R code based on the provided parameters to read a preprocessed data file,
    generate a pointplot, and save the resulting visualization as both a PNG and PDF file.

    Parameters:
    - infile (str, optional): Path to the input CSV file containing preprocessed data. Default is 'processed_stats.tsv'.
    - output (str, optional): Prefix for the output image filenames. Default is 'pointplot'.
    - x_lab (str, optional): Label for the x-axis. Default is 'Genomes'.
    - y_lab (str, optional): Label for the y-axis. Default is 'Families'.
    - title (str, optional): Title for the plot. Default is ''.
    - legend_title (str, optional): Title for the legend. Default is 'Type'.
    - dpi (int, optional): Resolution for the saved images. Default is 300.
    - width (int, optional): Width of the saved images in inches. Default is 14.
    - height (int, optional): Height of the saved images in inches. Default is 7.
    - **kwargs: Additional keyword arguments.

    Returns:
    - str: Generated R code.
    """
    script = R_CODE_TPL.substitute(**locals())
    return script
