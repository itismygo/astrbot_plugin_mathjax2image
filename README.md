# Mathjax2image

/mj2i 调用llm来生成支持mathjax的文章，并渲染为图片



/m2i 将带有数学公式的输入转化为输出（最后输出的都是和数学相关的）

例如/m2i 对于在环形区域 $R_1 < |z-a| < R_2$ 内解析的函数 $f(z)$，
$f(z)$ 具有唯一的 Laurent 级数展开：

$$
f(z) = \sum_{n=-\infty}^{\infty} c_n (z-a)^n
$$

其中系数 $c_n$ 由下式给出：

$$
c_n = \frac{1}{2\pi i} \oint_{\gamma} \frac{f(\zeta)}{(\zeta-a)^{n+1}} d\zeta, \quad n \in \mathbb{Z}
$$

这里的 $\gamma$ 是环形区域内任意一条围绕 $a$ 的简单闭合曲线。




/wz 调用llm生成文章（输出不一定是和数学相关的，不支持mathjax）



# 支持

[帮助文档](https://astrbot.app)
