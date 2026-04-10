"""
Ledom Layouter v1.3.0 (Dynamic Height & Interactive Lock Optimized)
Markdown to Word 文档转换工具
基于 Streamlit + Pandoc 实现
"""

import streamlit as st
import pypandoc
import os
import pyperclip
import tempfile
from datetime import datetime
from pathlib import Path

# --- 1. 全局配置 ---
st.set_page_config(
    page_title="Ledom Layouter v1.3.0",
    page_icon="📝",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. 交互式参数初始化 (必须在 CSS 引用前) ---
with st.sidebar:
    st.title("⚙️ 配置面板")
    # 高度调节滑块
    ui_height = st.slider(
        "📏 编辑器显示高度",
        min_value=400,
        max_value=1200,
        value=800,
        step=50
    )

# --- 3. 自定义 CSS 样式 (现在可以安全引用 ui_height) ---
st.markdown(f"""
    <style>
    /* 【核心修复1】彻底隐藏 text_area 的占位标签，实现编辑器与预览框的顶部完美对齐 */
    div[data-testid="stTextArea"] > label {{
        display: none !important;
        height: 0px !important;
        min-height: 0px !important;
    }}
    
    /* 编辑器样式优化 */
    .stTextArea textarea {{
        font-family: 'Consolas', 'Monaco', 'Fira Code', monospace;
        font-size: 14px;
        line-height: 1.6;
        height: {ui_height}px !important;
        min-height: {ui_height}px !important;
    }}
    
    /* 按钮统一样式 */
    .stButton > button {{
        width: 100%;
        height: 2.8rem !important;
        font-weight: 500;
        transition: all 0.2s ease;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-1px);
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }}
    
    /* 下载按钮特殊样式 */
    .stDownloadButton > button {{
        background-color: #28a745 !important;
        color: white !important;
        border: none;
    }}
    
    .stDownloadButton > button:hover {{
        background-color: #218838 !important;
        transform: translateY(-1px);
    }}
    
    /* 侧边栏优化 */
    .css-1d391kg {{
        padding-top: 2rem;
    }}
    
    /* 状态提示美化 */
    .stAlert {{
        border-radius: 8px;
        margin: 0.5rem 0;
    }}
    
    /* 进度条优化 */
    .stProgress > div {{
        border-radius: 8px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 2. 版本信息 ---
VERSION = "1.3.0"
APP_NAME = "Ledom Layouter"

# --- 3. 工具函数定义 ---

def check_pandoc():
    """检查 Pandoc 是否可用"""
    try:
        version = pypandoc.get_pandoc_version()
        return True, version
    except OSError:
        return False, None

def safe_convert(text, output_path, template_path, add_toc=False, num_sections=False):
    """安全的文档转换函数"""
    p_args = []
    
    if template_path and os.path.exists(template_path):
        safe_template = str(Path(template_path).resolve())
        p_args.append(f'--reference-doc={safe_template}')
    
    if add_toc:
        p_args.append('--toc')
    if num_sections:
        p_args.append('--number-sections')
    
    pypandoc.convert_text(
        text,
        'docx',
        format='md',
        outputfile=output_path,
        extra_args=p_args
    )

def handle_clipboard():
    """处理剪贴板读取"""
    try:
        content = pyperclip.paste()
        if content and content.strip():
            st.session_state.main_text = content
            st.toast("✅ 已从剪贴板同步内容", icon="📋")
        else:
            st.toast("⚠️ 剪贴板为空", icon="⚠️")
    except Exception as e:
        st.error(f"❌ 剪贴板访问失败: {str(e)}")
        st.info("💡 提示：请手动复制内容后粘贴到编辑区")

def handle_clear():
    """清空编辑区"""
    st.session_state.main_text = ""
    st.toast("🧹 已清空编辑区", icon="✨")

def handle_load_demo():
    """加载示例文档 - 完美修复 Markdown 逃逸漏洞"""
    # 动态生成反引号，防止聊天窗口渲染器提前截断代码块
    bk = chr(96) * 3 
    
    demo_text = "# Ledom Layouter 使用示例\n\n"
    demo_text += "## 功能介绍\n\n"
    demo_text += "这是一个 **Markdown 转 Word** 的专业工具，支持：\n\n"
    demo_text += "- 📝 实时编辑与预览\n"
    demo_text += "- 🎨 自定义 Word 模板样式\n"
    demo_text += "- 📋 剪贴板快速导入\n"
    demo_text += "- ⚙️ 高级排版参数\n\n"
    demo_text += "## 代码示例\n\n"
    demo_text += f"{bk}python\n"
    demo_text += "def hello_world():\n"
    demo_text += "    print(\"Hello, Ledom Layouter!\")\n"
    demo_text += f"{bk}\n\n"
    demo_text += "## 表格演示\n\n"
    demo_text += "| 功能 | 状态 | 说明 |\n"
    demo_text += "|------|------|------|\n"
    demo_text += "| 实时预览 | ✅ | 支持 |\n"
    demo_text += "| 模板支持 | ✅ | 需要 .docx 模板 |\n"
    demo_text += "| 目录生成 | ✅ | 可选功能 |\n\n"
    demo_text += "## 数学公式（需要 Pandoc 支持）\n\n"
    demo_text += "当 $a \\ne 0$ 时，方程 $ax^2+bx+c=0$ 的解为：\n\n"
    demo_text += "$$x = {-b \\pm \\sqrt{b^2-4ac} \\over 2a}$$\n\n"
    demo_text += "---\n\n"
    demo_text += "**开始你的文档创作吧！** 🚀\n"
    
    st.session_state.main_text = demo_text
    st.toast("📚 已加载示例文档", icon="🎯")

# --- 4. 环境初始化 ---
pandoc_available, pandoc_version = check_pandoc()
if not pandoc_available:
    st.error("""
    ❌ **未检测到 Pandoc**
    
    Ledom Layouter 依赖 Pandoc 进行文档转换，请先安装：
    
    - **Windows**: 下载安装包 https://pandoc.org/installing.html
    - **macOS**: `brew install pandoc`
    - **Linux**: `sudo apt-get install pandoc`
    
    安装完成后请重启应用。
    """)
    st.stop()

TEMPLATE_DIR = Path("templates")
TEMPLATE_DIR.mkdir(exist_ok=True)
available_templates = [f.name for f in TEMPLATE_DIR.glob("*.docx")]

# --- 5. 状态初始化 ---
if "main_text" not in st.session_state:
    st.session_state.main_text = ""
if "conversion_history" not in st.session_state:
    st.session_state.conversion_history = []
if "is_exporting" not in st.session_state:
    st.session_state.is_exporting = False

# --- 6. 侧边栏配置 ---
with st.sidebar:
    st.info(f"📌 **版本**: {VERSION}\n\n✅ **Pandoc**: {pandoc_version}")
    
    st.divider()
    
    st.subheader("📄 样式模板")
    if available_templates:
        selected_template = st.selectbox(
            "选择 Word 模板",
            available_templates,
            help="模板文件需放置在 templates 文件夹中"
        )
        
        with st.expander("ℹ️ 模板说明"):
            st.markdown("""
            **如何创建模板：**
            1. 新建 Word 文档
            2. 设置好标题、正文等样式
            3. 保存为 .docx 文件
            4. 放入 `templates` 文件夹
            
            **样式映射：**
            - `标题1` → 一级标题
            - `标题2` → 二级标题
            - `正文` → 普通文本
            """)
    else:
        st.warning("⚠️ 未检测到模板文件")
        st.info("请在 `templates` 文件夹中放入 .docx 模板文件")
        st.info("📌 放入模板后请按 F5 或点击浏览器刷新按钮")
        selected_template = None
        
        if st.button("📖 查看模板制作教程"):
            st.info("""
            1. 打开 Word 创建新文档
            2. 修改样式："开始" → "样式"
            3. 自定义"标题1"、"标题2"等样式
            4. 保存到 templates 文件夹
            """)
    
    st.divider()
    
    st.subheader("🔧 高级选项")
    add_toc = st.checkbox("📑 生成目录 (TOC)", value=False, help="自动生成文档目录")
    num_sections = st.checkbox("🔢 标题自动编号", value=False, help="为各级标题添加自动编号")
    
    st.divider()
    
    with st.expander("📖 关于"):
        st.markdown(f"""
        **{APP_NAME} v{VERSION}**
        
        基于 Streamlit + Pandoc 构建的 Markdown 转 Word 工具。
        
        **特性：**
        - 🚀 实时预览
        - 🎨 自定义模板
        - 📋 剪贴板集成
        - ⚡ 快速导出
        
        **开源协议:** MIT
        """)

# --- 7. 主界面布局 ---
st.title(f"📝 {APP_NAME}")
st.caption(f"版本 {VERSION} | 基于 Pandoc 的智能文档转换工具")

st.markdown("---")

col_actions = st.columns([1, 1, 1.2, 1.2, 1.5, 0.8])

with col_actions[0]:
    st.button("📋 读取剪贴板", on_click=handle_clipboard, use_container_width=True)

with col_actions[1]:
    st.button("🧹 清空编辑区", on_click=handle_clear, use_container_width=True)

with col_actions[2]:
    st.button("📚 加载示例", on_click=handle_load_demo, use_container_width=True)

with col_actions[3]:
    export_btn = st.button(
        "🚀 导出 Word",
        type="primary",
        disabled=st.session_state.get("is_exporting", False),
        use_container_width=True
    )

with col_actions[4]:
    download_container = st.empty()

with col_actions[5]:
    char_count = len(st.session_state.main_text)
    st.caption(f"📊 {char_count} 字符")

st.markdown("---")

# --- 8. 主体编辑区 ---
@st.fragment
def render_editor(h):
    col_edit, col_preview = st.columns(2, gap="small")
    
    with col_edit:
        st.subheader("✍️ Markdown 编辑器")
        st.caption("💡 支持标准 Markdown 语法，实时预览效果")
        st.text_area(
            "markdown_input",
            key="main_text",
            height=h,
            label_visibility="collapsed",
            placeholder="在此输入或粘贴 Markdown 内容...\n\n支持标题、列表、代码块、表格、公式等标准语法"
        )
        
        with st.expander("📝 Markdown 语法速查"):
            st.markdown("""
            - **标题**: `# H1`, `## H2`, `### H3`
            - **粗体**: `**粗体**`
            - **斜体**: `*斜体*`
            - **列表**: `- 无序`, `1. 有序`
            - **代码块**: 三个反引号 + 语言名
            - **链接**: `[文字](url)`
            - **图片**: `![alt](url)`
            - **表格**: 使用 `|` 分隔
            """)
    
    with col_preview:
        st.subheader("👁️ 实时预览")
        st.caption("💡 预览为 Markdown 渲染效果，最终样式以 Word 模板为准") # 【核心修复2】补齐左侧 caption 高度
        
        # 【核心修复3】废弃 CSS Hacks，使用官方原生容器，彻底避免溢出
        with st.container(height=h, border=True):
            if st.session_state.main_text and st.session_state.main_text.strip():
                st.markdown(st.session_state.main_text)
            else:
                st.info("💡 等待输入内容...")
    
    if st.session_state.main_text and st.session_state.main_text.strip():
        lines = len(st.session_state.main_text.split('\n'))
        words = len(st.session_state.main_text.split())
        st.caption(f"📊 统计信息：{lines} 行 | {words} 词 | {char_count} 字符")

render_editor(ui_height)

# --- 9. 导出逻辑 ---
if export_btn and not st.session_state.is_exporting:
    if not st.session_state.main_text or not st.session_state.main_text.strip():
        st.toast("⚠️ 编辑区内容为空，请先输入内容", icon="⚠️")
    elif not selected_template:
        st.toast("📄 请先在侧边栏选择一个 Word 模板", icon="⚠️")
    else:
        try:
            st.session_state.is_exporting = True
            progress_bar = st.progress(0, "准备转换...")
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            out_filename = f"{APP_NAME}_{timestamp}.docx"
            
            with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as tmp_file:
                out_path = tmp_file.name
            
            progress_bar.progress(30, "正在应用模板样式...")
            tmpl_path = TEMPLATE_DIR / selected_template
            
            try:
                safe_convert(
                    st.session_state.main_text,
                    out_path,
                    tmpl_path,
                    add_toc,
                    num_sections
                )
                progress_bar.progress(80, "生成文档文件...")
                with open(out_path, "rb") as f:
                    file_data = f.read()
            finally:
                if os.path.exists(out_path):
                    try: os.unlink(out_path)
                    except: pass
            
            # 【关键修改 1】：将生成的数据和文件名持久化到 session_state
            st.session_state.export_data = file_data
            st.session_state.export_filename = out_filename
            
            st.session_state.conversion_history.append({
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "filename": out_filename,
                "size": len(file_data),
                "template": selected_template
            })
            
            progress_bar.progress(100, "✅ 转换完成！")
            st.balloons()
            st.toast("🎉 文档生成成功！点击下载按钮保存文件", icon="✅")
            
        except pypandoc.PandocError as e:
            st.error(f"❌ Pandoc 转换失败：{str(e)}")
            st.info("💡 提示：请检查 Markdown 语法是否正确，或尝试简化内容后重新转换")
        except Exception as e:
            st.error(f"❌ 转换异常：{str(e)}")
            st.info("💡 提示：如问题持续出现，请检查模板文件是否损坏")
        finally:
            if "progress_bar" in locals():
                progress_bar.empty()
            st.session_state.is_exporting = False

# 【关键修改 2】：在 if 块外部，独立渲染下载按钮
if st.session_state.get("export_data"):
    with download_container:
        st.download_button(
            label=f"📥 下载 {st.session_state.export_filename}",
            data=st.session_state.export_data,
            file_name=st.session_state.export_filename,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            use_container_width=True
        )

# --- 10. 转换历史显示 ---
if st.session_state.conversion_history and st.sidebar.checkbox("显示转换历史", value=False):
    with st.sidebar:
        st.divider()
        
        # 优化布局：标题与清空按钮并排
        h_col1, h_col2 = st.columns([1.5, 1])
        with h_col1:
            st.subheader("📜 转换历史")
        with h_col2:
            if st.button("🗑️ 清空", use_container_width=True):
                st.session_state.conversion_history = []
                st.rerun()
                
        for record in st.session_state.conversion_history[-5:]:
            st.caption(f"🕐 {record['time']}")
            st.caption(f"📄 {record['filename']}")
            st.caption(f"📏 {record['size'] // 1024} KB")
            st.divider()

# --- 11. 页脚信息 ---
st.markdown("---")
st.caption(f"💡 提示：Ledom Layouter v{VERSION} | 使用 Pandoc {pandoc_version} 引擎 | 支持自定义 Word 模板")