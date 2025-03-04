from manim import *
import numpy as np




# 定义复函数
def complex_function(z):
    # f(z) = z^2 + z
    return (z**3 - z**2 + z)*complex(0, 1)
    # return np.sin(z)

# 定义复函数对应的 latex 文本公式
latex_formula = "f(z) = (z^3 - z^2 + z)\mathbf{i}"
# latex_formula = "f(z) = \sin(z)"

# 定义复函数自变量的范围
z_scale = 1.0






# 复函数可视化演示
class ComplexFunctionVisualization(Scene):
    def construct(self):
        
        # 创建复平面
        complex_plane = ComplexPlane(
            x_range=[-8, 8, 1],
            y_range=[-8, 8, 1],
            background_line_style={
                "stroke_color": BLUE_D,
                "stroke_width": 1,
                "stroke_opacity": 0.6
            }
        ).scale(1.0)
        
        # 添加坐标轴标签
        complex_plane.add_coordinates()
        
        # 函数公式文本
        function_formula = MathTex(latex_formula).to_corner(UL).set_color(WHITE)
        
        # 路径类型文本（初始为空，后续会更新）
        path_type = Text("").to_corner(UR).set_color(WHITE)
        
        # 添加复平面和函数公式
        self.play(Create(complex_plane), Write(function_formula))
        self.wait(1)
        
        label_obj = None
        # 1. 矩形路径演示
        self.demonstrate_path(
            complex_plane, complex_function, 
            path_type, "矩形路径", 
            self.create_rectangle_path,
        )
        
        # 2. 圆形路径演示
        self.demonstrate_path(
            complex_plane, complex_function, 
            path_type, "圆形路径", 
            self.create_circle_path,
        )
        
        # 3. 径向路径演示
        self.demonstrate_path(
            complex_plane, complex_function, 
            path_type, "径向路径", 
            self.create_radial_path,
        )
        
        # 4. 阿基米德螺线路径演示
        self.demonstrate_path(
            complex_plane, complex_function, 
            path_type, "阿基米德螺线", 
            self.create_archimedes_spiral_path,
        )
        
        self.wait(2)
    
    def demonstrate_path(self, complex_plane, function, path_type_text, path_name, path_creator):
        """演示特定路径上的函数变化
        
        参数:
            complex_plane: 复平面对象
            function: 复函数
            path_type_text: 路径类型文本对象
            path_name: 路径名称
            path_creator: 创建路径的函数
        """
        path_type_text = Text(path_name).to_corner(UR).set_color(WHITE)

        self.play(Write(path_type_text))
        # 创建路径
        z_path, start_point = path_creator()
        
        # 创建表示 z 和 f(z) 的点
        z_dot = Dot(complex_plane.n2p(start_point), color=RED)
        f_dot = Dot(complex_plane.n2p(function(start_point)), color=YELLOW)
        
        # 添加标签
        z_label = MathTex("z").next_to(z_dot, DOWN).set_color(RED)
        f_label = MathTex("f(z)").next_to(f_dot, DOWN).set_color(YELLOW)
        
        # 创建路径跟踪
        z_path_trace = TracedPath(z_dot.get_center, stroke_width=3, stroke_color=RED)
        f_path_trace = TracedPath(f_dot.get_center, stroke_width=3, stroke_color=YELLOW)
        
        # 添加点和路径跟踪
        self.play(
            Create(z_dot), Create(f_dot),
            Write(z_label), Write(f_label),
            Create(z_path_trace), Create(f_path_trace)
        )
        
        # 创建动画
        def update_f_dot(mob):
            # 获取 z 的复数值
            z_pos = complex_plane.p2n(z_dot.get_center())
            # 计算 f(z) 的值
            f_z = function(z_pos)
            # 更新 f(z) 点的位置
            mob.move_to(complex_plane.n2p(f_z))
            # 更新 f(z) 标签的位置
            f_label.next_to(mob, DOWN)
        
        # 设置 f_dot 的更新函数
        f_dot.add_updater(update_f_dot)
        
        # 沿路径移动 z 点
        self.play(
            MoveAlongPath(z_dot, z_path),
            UpdateFromFunc(z_label, lambda m: m.next_to(z_dot, DOWN)),
            run_time=10
        )
        
        # 移除更新器
        f_dot.clear_updaters()
        
        # 暂停一下
        self.wait(1)
        
        # 清除点和路径
        self.play(
            FadeOut(z_dot), FadeOut(f_dot),
            FadeOut(z_label), FadeOut(f_label),
            FadeOut(z_path_trace), FadeOut(f_path_trace), 
            FadeOut(path_type_text)
        )        
    
    def create_rectangle_path(self):
        """创建矩形路径
        
        返回:
            tuple: (路径对象, 起始点)
        """
        # 矩形的四个顶点（复平面坐标）
        rect_points = [
            complex(-1, -1)*z_scale,  # 左下
            complex(1, -1)*z_scale,   # 右下
            complex(1, 1)*z_scale,    # 右上
            complex(-1, 1)*z_scale,   # 左上
            complex(-1, -1)*z_scale   # 回到起点
        ]
        
        # 创建矩形路径
        vertices = [np.array([p.real, p.imag, 0]) for p in rect_points]
        rectangle = VMobject()
        rectangle.set_points_as_corners(vertices)
        
        return rectangle, rect_points[0]
    
    def create_circle_path(self):
        """创建圆形路径
        
        返回:
            tuple: (路径对象, 起始点)
        """
        # 圆的参数
        radius = 1*z_scale
        center = complex(0, 0)
        start_point = center + radius
        
        # 创建圆形路径
        circle = Circle(radius=radius)
        
        return circle, start_point
    
    def create_radial_path(self):
        """创建径向路径（从原点向外辐射的直线）
        
        返回:
            tuple: (路径对象, 起始点)
        """
        # 径向路径参数
        num_rays = 8  # 径向线的数量
        ray_length = z_scale  # 径向线的长度
        
        # 创建径向路径（多条从原点出发的直线）
        radial_path = VMobject()
        
        # 为每条径向线创建点集
        all_points = []
        for i in range(num_rays):
            angle = i * 2 * PI / num_rays
            # 从原点到目标点
            start_point = np.array([0, 0, 0])
            end_point = np.array([ray_length * np.cos(angle), ray_length * np.sin(angle), 0])
            
            # 添加去程路径点
            all_points.append(start_point)
            all_points.append(end_point)
            
            # 如果不是最后一条径向线，添加回程路径点
            if i < num_rays - 1:
                all_points.append(start_point)
        
        # 设置路径点
        radial_path.set_points_as_corners(all_points)
        
        # 起始点为原点
        start_point = complex(0, 0)
        
        return radial_path, start_point
    
    def create_archimedes_spiral_path(self):
        """创建阿基米德螺线路径
        
        返回:
            tuple: (路径对象, 起始点)
        """
        # 螺线参数
        a = 0.15*z_scale  # 螺线系数
        max_theta = 4 * PI  # 最大角度
        
        # 参数方程: r = a * theta
        def spiral_func(t):
            theta = t * max_theta
            r = a * theta
            x = r * np.cos(theta)
            y = r * np.sin(theta)
            return np.array([x, y, 0])
        
        # 创建螺线路径 - 修复 scaling 参数问题
        spiral = ParametricFunction(
            spiral_func,
            t_range=[0, 1, 0.01],  # 使用三元组格式 [t_min, t_max, t_step]
        )
        
        # 起始点 (t=0)
        start_point = complex(0, 0)
        
        return spiral, start_point


# 主函数
if __name__ == "__main__":
    # 使用命令行运行: manim -pql complex_function_visualization.py ComplexFunctionVisualization
    print("请使用以下命令运行动画:")
    print("manim -qh complex_function_visualization.py ComplexFunctionVisualization") 