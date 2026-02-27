import streamlit as st
from openai import OpenAI
import time
import json
import os
import sys

# Ensure current directory is in path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

try:
    from clash_data import ClashData
except ImportError:
    # Fallback or simple error handling if file missing
    st.error("Failed to import clash_data. Please ensure clash_data.py is in the same directory.")
    ClashData = None

# 1. 页面配置与风格设置
st.set_page_config(
    page_title="Clash of Clans AI Wiki",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS，增强游戏风格（深色背景、卡片样式）
st.markdown("""
<style>
    /* 全局深色背景微调 */
    .stApp {
        background-color: #0e1117;
    }
    
    /* 按钮样式模仿游戏按钮 */
    .stButton > button {
        background-color: #2b313e;
        color: #ffffff;
        border: 2px solid #4a5568;
        border-radius: 10px;
        font-weight: bold;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        background-color: #4a5568;
        border-color: #63b3ed;
        transform: scale(1.02);
    }
    
    /* 标题样式 */
    h1, h2, h3 {
        color: #fbd38d !important; /* 金色字体 */
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        text-shadow: 2px 2px 4px #000000;
    }
    
    /* 侧边栏样式 */
    [data-testid="stSidebar"] {
        background-color: #1a202c;
        border-right: 1px solid #2d3748;
    }
    
    /* 选中状态的高亮 */
    .highlight-card {
        border: 2px solid #fbd38d;
        padding: 10px;
        border-radius: 10px;
        background-color: #2d3748;
    }
    
    /* 
    header[data-testid="stHeader"]{
        display:none;
    }
    */
    footer{
        display:none;
    }
    .stDeployButton
    {display:none;}
    #MainMenu {visibility:hidden}


</style>
""", unsafe_allow_html=True)

# 2. 数据结构：分类与物品
@st.cache_resource
def get_clash_data_loader():
    if ClashData:
        return ClashData()
    return None

data_loader = get_clash_data_loader()

# 2. 数据结构：分类与物品
CATEGORIES = {
    "防御建筑 ": {
        "icon": "🏠",
        "items": ["大本营" ,"城墙" ,"加农炮" ,"箭塔" ,"迫击炮" ,"防空火箭" ,"法师塔" ,"空气炮" ,"特斯拉电磁塔" ,"炸弹塔" ,"X连弩" ,"地狱之塔" ,"天鹰火炮" ,"投石炮" ,"建筑工人小屋" ,"法术塔" ,"巨石碑" ,"跳弹加农炮" ,"多人箭塔" ,"火焰喷射器" ,"复合机械塔" ,"超级法师塔" ,"复仇之塔"]
    },
    "陷阱":{
        "icon":"💣",
        "items":["隐形炸弹","隐形弹簧","空中炸弹","巨型炸弹","搜空地雷","骷髅陷阱","飓风陷阱","终极炸弹"]
    },
    "资源类建筑":{
        "icon": "🏠",
        "items": ["金圣水收集器","暗黑重油钻井","储金罐","圣水瓶","暗黑重油罐","部落城堡"]
    },
    "军事建筑":{
        "icon":"🏠",
        "items":["兵营","训练营","暗黑训练营","实验室","法术工厂","暗黑法术工厂","攻城机器工坊","战宠小屋","铁匠铺","英雄殿堂","精制台"]
    },
    "军队 (Army)": {
        "icon": "⚔️",
        "items": ["野蛮人 (Barbarian)", "弓箭手 (Archer)", "巨人 (Giant)", "哥布林 (Goblin)", "炸弹人 (Wall Breaker)", "气球兵 (Balloon)", "法师 (Wizard)", "天使 (Healer)", "飞龙 (Dragon)", "皮卡超人 (P.E.K.K.A)", "飞龙宝宝 (Baby Dragon)", "矿工 (Miner)", "雷电飞龙 (Electro Dragon)", "大雪怪 (Yeti)", "龙骑 (Dragon Rider)", "雷电泰坦 (Electro Titan)", "根蔓骑士 (Root Rider)",
         "根蔓骑士","巨矛投手","陨石戈仑" ,"亡灵","野猪骑士","瓦基丽武神","戈仑石人","女巫","熔岩猎犬","巨石投手","戈仑冰人","英雄猎手","守护者学徒","德鲁伊","烈焰熔炉"]},
    "超级兵":{
        "icon":"⚔",
        "items":["超级野蛮人","超级弓箭手","超级巨人","隐秘哥布林","超级炸弹人","火箭气球兵","超级法师","超级飞龙","地狱飞龙","超级矿工","超级大雪怪","超级亡灵","超级野猪骑士","超级瓦基丽武神","超级女巫","寒冰猎犬","超级巨石投手 "        
    ]},
    "法术 (Spells)": {
        "icon": "🧪",
        "items": ["雷电法术 (Lightning Spell)", "疗伤法术 (Healing Spell)", "狂暴法术 (Rage Spell)", "弹跳法术 (Jump Spell)", "冰冻法术 (Freeze Spell)", "克隆法术 (Clone Spell)", "隐形法术 (Invisibility Spell)", "回溯法术 (Recall Spell)","复苏法术" ,"图腾法术","毒药法术 (Poison Spell)", "地震法术 (Earthquake Spell)", "急速法术 (Haste Spell)", "骷髅法术 (Skeleton Spell)", "蝙蝠法术 (Bat Spell)", "蔓生法术 (Overgrowth Spell)","冰障法术"]
    },
    "攻城机器":{
        "icon":"🚂",
        "items":["攻城战车","攻城飞艇","攻城气球","攻城训练营","攻城滚木车","攻城烈焰车","攻城钻机","部队发射器"]
    },
    "英雄 (Heroes)": {
        "icon": "🦸",
        "items": ["野蛮人之王 (Barbarian King)", "弓箭女皇 (Archer Queen)","亡灵王子","大守护者 (Grand Warden)", "飞盾战神 (Royal Champion)"]
    },
    "夜世界军事建筑":{
        "icon":"⛪",
        "items":["兵营","建筑大师训练营","预备营","星空实验室","治疗小屋"]
    },
    "夜世界军队 (Army)": {
        "icon": "⚔️",
        "items": ["狂暴野蛮人 (Barbarian)", "隐秘弓箭手 (Archer)", "巨人拳击手 (Giant)" "炸弹兵 (Wall Breaker)", "骷髅气球 ", "电火法师 (Wizard)", "雷霆皮卡 ", "飞龙宝宝 (Baby Dragon)","加农炮战车",  
         "异变亡灵","野猪飞骑","暗夜女巫"]},
    "夜世界英雄 (Heroes)": {
        "icon": "🦸",
        "items": ["战争机器", "战斗直升机"]
    },
    "夜世界防御建筑 ": {
        "icon": "🏠",
        "items": ["城墙" ,"加农炮" ,"双管加农炮" ,"箭塔" ,"多管迫击炮" ,"防空火箭"  ,"特斯拉电磁塔" ,"撼地巨石","守卫岗哨",
        "空中炸弹发射器","熔岩火炮","巨型加农炮","超级特斯拉电磁塔","熔岩发射器","X连弩"]
    },
    "夜世界陷阱":{
        "icon":"💣",
        "items":["隐形炸弹","隐形弹簧","巨型炸弹","弹射陷阱"]
    },
    "夜世界资源类建筑":{
        "icon": "🏠",
        "items": ["金圣水收集器","储金罐","圣水瓶"]
    },

}
# 3. 侧边栏逻辑
with st.sidebar:
    st.markdown("## ⚙️ 设置")
    api_key = st.text_input("DeepSeek API Key", type="password", placeholder="sk-...", help="请输入您的 DeepSeek API Key 以启用 AI 功能")
    
    st.markdown("---")
    st.markdown("## 🗺️ 导航")
    
    # 分类选择
    selected_category_name = st.radio(
        "选择分类",
        options=list(CATEGORIES.keys()),
        format_func=lambda x: f"{CATEGORIES[x]['icon']} {x.split(' (')[0]}"
    )
    
    st.markdown("---")
    st.markdown("Build with ❤️ by Streamlit & DeepSeek")

# 4. 主界面逻辑
st.title("🛡️ Clash of Clans AI Wiki ⚔️")

if not api_key:
    st.warning("⚠️ 请在左侧侧边栏输入 DeepSeek API Key 才能召唤哥布林工程师！")
    st.stop()

# 初始化 session state 用于存储选中的物品
if 'selected_item' not in st.session_state:
    st.session_state.selected_item = None
if 'current_category' not in st.session_state:
    st.session_state.current_category = selected_category_name

# 如果切换了分类，重置选中的物品
if st.session_state.current_category != selected_category_name:
    st.session_state.selected_item = None
    st.session_state.current_category = selected_category_name

# 布局容器
col_nav, col_detail = st.columns([1, 1.5])

with col_nav:
    st.subheader(f"{CATEGORIES[selected_category_name]['icon']} {selected_category_name.split(' (')[0]}")
    
    # 获取当前分类下的物品列表
    items = CATEGORIES[selected_category_name]["items"]
    
    # Grid 布局显示物品按钮
    cols = st.columns(3)
    for idx, item_name in enumerate(items):
        with cols[idx % 3]:
            # 提取简短名称用于按钮显示
            short_name = item_name.split(' (')[0]
            if st.button(short_name, key=f"btn_{item_name}", use_container_width=True):
                st.session_state.selected_item = item_name

# 5. 详情与 AI 生成逻辑
with col_detail:
    if st.session_state.selected_item:
        item_full_name = st.session_state.selected_item
        st.markdown(f"## 📜 {item_full_name} 档案")
        
        # 显示加载动画
        with st.status(f"🤖 正在召唤哥布林工程师计算 {item_full_name} 的数据...", expanded=True) as status:
            st.write("📡 连接部落服务器...")
            time.sleep(0.5)
            st.write("📚 翻阅古老卷轴...")
            
            try:
                # 初始化 OpenAI 客户端 (DeepSeek 兼容)
                client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
                
                # 获取该物品的 JSON 数据
                item_data = None
                if data_loader:
                    item_data = data_loader.get_data(item_full_name)
                
                # 构建 Prompt
                system_prompt = """你是一个部落冲突 (Clash of Clans) 资深玩家和游戏专家。
                你的说话风格幽默风趣，必须大量使用 Emoji 表情来活跃气氛。
                你非常擅长整理数据，能够清晰地列出兵种或建筑的详细属性。
                
                """
                
                if item_data:
                    system_prompt += f"\n\n请务必参考以下官方数据 (JSON格式) 来回答用户的问题，特别是数值属性：\n{json.dumps(item_data, ensure_ascii=False)}"
                
                system_prompt += """
                
                请按照以下格式介绍用户指定的单位：
                1. **开场白**：用一句幽默的话介绍这个单位，带上 Emoji。
                2. **玩法技巧**：简要介绍它的特点和使用/防御技巧 (Bullet points)。
                3. **数量上限表**：创建一个 Markdown 表格，列出不同大本营等级下该建筑/单位的可建造数量上限（如果是兵种，则列出该兵种在不同大本营解锁的等级）。
                4. **全部升级数据**：创建一个 Markdown 表格，列出全部属性随等级变化的数据（列出所有）。
                
                请确保表格格式规范，Markdown 渲染正常。"""
                
                user_prompt = f"请详细介绍：{item_full_name}"
                
                # 调用 API
                response = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    stream=True
                )
                
                status.update(label="✅ 数据生成完毕！", state="complete", expanded=False)
                
                # 流式输出结果
                st.write_stream(response)
                
            except Exception as e:
                status.update(label="❌ 哥布林工程师罢工了！", state="error")
                st.error(f"发生错误: {str(e)}")
                if "401" in str(e):
                    st.error("请检查您的 API Key 是否正确。")
    else:
        # 初始状态提示
        st.info("👈 请在左侧选择一个单位查看详细数据")
        st.markdown("""
        ### ✨ 欢迎来到 AI 维基百科
        这里没有枯燥的数据，只有最生动的 **AI 实时生成** 攻略！
        
        1. 在侧边栏输入 **DeepSeek API Key**
        2. 选择感兴趣的 **分类**
        3. 点击具体的 **兵种** 或 **建筑**
        4. 见证魔法发生！ 🧙‍♂️
        """)

 
