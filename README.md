# 复函数可视化演示

这个项目使用 Manim 库创建了一个复函数映射的可视化演示。通过动画方式展示复变函数在不同路径上的映射关系，帮助理解复分析中的函数行为。

## 功能特点

- **复平面可视化**：在二维平面上展示复数的实部和虚部
- **多种路径演示**：包括矩形、圆形、径向和阿基米德螺线等多种路径
- **实时映射**：直观展示输入点 z 和输出点 f(z) 的对应关系
- **轨迹跟踪**：通过彩色轨迹清晰展示映射前后的路径变化
- **可配置参数**：可以方便地修改函数表达式和路径参数

## 演示内容

该程序演示了复函数 f(z) = (z³ - z² + z)i 在以下路径上的映射关系：

1. **矩形路径**：在复平面上沿矩形边界移动
2. **圆形路径**：在复平面上沿圆周移动
3. **径向路径**：从原点沿不同角度的径向线移动
4. **阿基米德螺线**：沿螺旋线从原点向外移动

每种路径演示都会显示：
- 红色点表示输入值 z 及其轨迹
- 黄色点表示输出值 f(z) 及其轨迹
- 左上角显示函数表达式
- 右上角显示当前路径类型

## 安装说明

### 前提条件

- Python 3.7 或更高版本
- pip 包管理器

### 安装步骤

1. 克隆此仓库：
   ```bash
   git clone https://github.com/yourusername/complex-function-visualization.git
   cd complex-function-visualization
   ```

2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

### 可能的系统依赖

Manim 可能需要一些系统依赖，如 FFmpeg、LaTeX 等。请参考 [Manim 安装指南](https://docs.manim.community/en/stable/installation.html) 获取详细信息。

## 使用方法

1. 运行演示：
   ```bash
   manim -qh complex_function_visualization.py ComplexFunctionVisualization
   ```

   参数说明：
   - `-q`：设置质量（h=高质量，m=中等质量，l=低质量）
   - `-p`：生成后自动播放

2. 修改函数：
   
   编辑 `complex_function_visualization.py` 文件顶部的 `complex_function` 函数和 `latex_formula` 变量来更改演示的函数。

3. 调整参数：

   修改 `z_scale` 变量可以调整所有路径的大小。

## 自定义

### 修改函数

要更改演示的复函数，请编辑文件顶部的以下部分：

```python
# 定义复函数
def complex_function(z):
    return (z**3 - z**2 + z)*complex(0, 1)
    # return np.sin(z)  # 取消注释以使用正弦函数

# 定义复函数对应的 latex 文本公式
latex_formula = "f(z) = (z^3 - z^2 + z)\mathbf{i}"
# latex_formula = "f(z) = \sin(z)"
```

### 添加新路径

要添加新的路径类型，请：

1. 创建一个新的路径生成方法，类似于 `create_rectangle_path`
2. 在 `construct` 方法中添加对 `demonstrate_path` 的调用

## 贡献指南

欢迎贡献！如果您想改进这个项目，请：

1. Fork 这个仓库
2. 创建您的特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交您的更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启一个 Pull Request

## 许可证

本项目采用 MIT 许可证 - 详情请参阅 [LICENSE](LICENSE) 文件。

## 致谢

- [Manim 社区](https://www.manim.community/) - 提供了强大的数学动画库
- 所有复分析的教育工作者和学习者 