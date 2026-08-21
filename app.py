import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# 设置页面配置
st.set_page_config(
    page_title="智能水培营养液配方计算器 v4",
    page_icon="🍀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 网站标题和介绍
st.title("🍀 智能水培营养液配方计算器 (Web v4 - 雷达对比图流量黄金版)")
st.markdown("""
通过这套系统，您可以快速计算不同作物在各生长阶段所需的 A/B 母液配比。
本工具基于 **J. Benton Jones Jr. 经典水培营养学原理**、学术界经典 **Hoagland No. 2** 配方、Reddit 社区高赞验证配方，并融合了 **NASA 太空微重力培养数据**。
""")

# 侧边栏：核心输入参数
st.sidebar.header("⚙️ 调配参数设置")

# 1. 选择作物和配方分类
crop_category = st.sidebar.selectbox(
    "1. 选择作物分类",
    ["生菜 (Lettuce) - 绿叶菜黄金通道", "西红柿 (Tomato) - 挂果高值通道", "太空模拟 (Space Farms) - 极客引流卖点"]
)

if crop_category == "生菜 (Lettuce) - 绿叶菜黄金通道":
    recipe_options = [
        "生菜 - Kratky 极简免维护配方 (最适合阳台新手)",
        "生菜 - 商业级 NFT/垂直塔高产高氮配方 (促叶生长期)"
    ]
elif crop_category == "西红柿 (Tomato) - 挂果高值通道":
    recipe_options = [
        "西红柿 - Hoagland No. 2 学术级黄金平衡配方",
        "西红柿 - 挂果中后期“限氮促花”强效配方 (防脐腐病)"
    ]
else:
    recipe_options = [
        "太空模拟豌豆 - Microgravity Sim 🌌 (NASA低重力调配)"
    ]

recipe = st.sidebar.selectbox("2. 选择具体生长配方", recipe_options)

# 2. 输入水量
st.sidebar.markdown("---")
unit = st.sidebar.radio("3. 选择水量单位", ["升 (L)", "加仑 (GAL)"], index=0)
volume = st.sidebar.number_input("4. 输入最终稀释总体积", min_value=1.0, value=100.0, step=10.0)

# 单位转换：将加仑转换为升进行统一计算 (1 Gallon ≈ 3.785 Liters)
volume_in_liters = volume if unit == "升 (L)" else volume * 3.78541

# 3. 目标 EC 调节与生长阶段微调
st.sidebar.markdown("---")
st.sidebar.subheader("📈 生长阶段与浓度微调")

# 设定不同配方的默认值、范围和提示信息
if "Kratky" in recipe:
    default_ec = 1.4
    min_ec, max_ec = 0.8, 1.8
    st.sidebar.info("💡 Kratky 极简配方推荐 EC：1.2 - 1.6 mS/cm。该方法无需气泵，适合静止水培。")
elif "商业级" in recipe:
    default_ec = 1.5
    min_ec, max_ec = 1.0, 2.0
    st.sidebar.info("💡 商业 NFT 循环系统需要较高氮肥，推荐 EC：1.4 - 1.8 mS/cm，促进叶片快速膨大。")
elif "Hoagland" in recipe:
    default_ec = 2.0
    min_ec, max_ec = 1.5, 2.5
    st.sidebar.info("💡 霍格兰二号是学术界黄金标尺。全阶段平衡配方，推荐 EC：1.8 - 2.2 mS/cm。")
elif "限氮促花" in recipe:
    default_ec = 2.2
    min_ec, max_ec = 1.8, 2.8
    st.sidebar.info("💡 挂果中后期大幅度提高磷钾、限制氮源以诱导极速开花结果，推荐高 EC：2.0 - 2.5 mS/cm，并可有效防止西红柿脐腐病。")
else:
    # 太空豌豆配方
    default_ec = 1.8
    min_ec, max_ec = 1.2, 2.4
    st.sidebar.info("🛸 太空微重力下二价阳离子（钙镁铁）吸收受阻，而单价阴阳离子（磷钾）吸收异常激增。推荐 EC：1.6 - 2.0 mS/cm。")

target_ec = st.sidebar.slider(
    "设定目标电导率 (EC, mS/cm)",
    min_value=min_ec,
    max_value=max_ec,
    value=default_ec,
    step=0.1
)

# 4. 水质 pH 预警
st.sidebar.markdown("---")
st.sidebar.subheader("🧪 初始水源 pH 监测")
water_ph = st.sidebar.slider("您的水源初始 pH 值", min_value=4.0, max_value=8.5, value=6.5, step=0.1)

# 开始计算配方
st.subheader(f"📊 {recipe} - 专属配方计算结果")

# 定义不同配方的基础数据 (基于 100 升水以及各自的基准 EC)
if "Kratky" in recipe:
    base_calc = {
        "Ca(NO3)2": 28.0 / 15.14,
        "KNO3": 12.0 / 15.14,
        "MgSO4": 12.0 / 15.14,
        "KH2PO4": 2.0 / 15.14,
        "Trace": 16.0 / 15.14,
        "Fe_EDDHA": 1.5 / 15.14,
    }
    base_ec_val = 1.4
    explain_a = ["提供植株骨架发育的钙源（100% 硝态氮）", "Kratky 系统中温和、不烧根的高效钾氮源"]
    explain_b = [
        "维持静止水培下叶片叶绿素合成",
        "极低剂量磷源，防止前期疯长，保证根系舒展",
        "提供微量元素补充，防止黄化",
        "螯合铁防止静止营养液高 pH 沉淀 lockout"
    ]
elif "商业级" in recipe:
    base_calc = {
        "Ca(NO3)2": 65.0 / 100.0,
        "KNO3": 30.0 / 100.0,
        "MgSO4": 40.0 / 100.0,
        "KH2PO4": 15.0 / 100.0,
        "Trace": 5.0 / 100.0,
        "Fe_EDDHA": 2.0 / 100.0,
    }
    base_ec_val = 1.4
    explain_a = ["商业 NFT 高产的高效硝态氮，促进叶绿素积累", "超高溶解度钾源，在水流循环中为茎叶极速泵送养分"]
    explain_b = [
        "支持强光照垂直塔系统下的镁硫高消耗",
        "提供充足的磷源，促进快速分蘖与多叶叶盘形成",
        "高度适配流速系统的微量元素补充",
        "螯合铁防止营养液频繁流动与空气接触导致的氧化沉淀"
    ]
elif "Hoagland" in recipe:
    base_calc = {
        "Ca(NO3)2": 82.0 / 100.0,
        "KNO3": 50.0 / 100.0,
        "MgSO4": 49.0 / 100.0,
        "KH2PO4": 14.0 / 100.0,
        "Trace": 5.0 / 100.0,
        "Fe_EDDHA": 2.5 / 100.0,
    }
    base_ec_val = 2.0
    explain_a = ["学术界番茄防脐腐病的标准钙水平 (约 150-200 ppm)", "平衡生长全阶段所需的标准钾与硝态氮比例"]
    explain_b = [
        "提供稳定的镁源，防止老叶叶脉间缺镁黄化",
        "经典 31 ppm 磷酸盐水平，维持健康的根系与细胞分裂",
        "提供经典的霍格兰无机微量元素群",
        "高稳定性螯合铁，确保光合作用最高效能"
    ]
elif "限氮促花" in recipe:
    base_calc = {
        "Ca(NO3)2": 50.0 / 100.0,   
        "KNO3": 45.0 / 100.0,
        "MgSO4": 50.0 / 100.0,
        "KH2PO4": 35.0 / 100.0,      
        "Trace": 6.0 / 100.0,
        "Fe_EDDHA": 3.0 / 100.0,
    }
    base_ec_val = 2.2
    explain_a = ["适度限氮，防止西红柿挂果后期枝叶疯长、营养徒长", "高水平钾元素，强效膨果，增加番茄红素与干物质积累"]
    explain_b = [
        "保障高产挂果期的叶片能量代谢",
        "超高磷配比，强效诱导花芽分化，实现极致的果实饱满度",
        "挂果期高消耗微量元素补偿",
        "螯合铁防沉淀高强度升级，保障高蒸腾作用下的叶绿素密度"
    ]
else:
    # 太空模拟豌豆
    base_calc = {
        "Ca(NO3)2": 110.0 / 100.0,  
        "KNO3": 25.0 / 100.0,       
        "MgSO4": 80.0 / 100.0,      
        "KH2PO4": 10.0 / 100.0,     
        "Trace": 8.0 / 100.0,       
        "Fe_EDDHA": 3.0 / 100.0,    
    }
    base_ec_val = 1.8
    explain_a = ["太空微重力吸收效率降低，大幅上调钙源补偿植株骨架", "调低钾比例，防止微重力极速高吸收引起的钾中毒"]
    explain_b = [
        "太空低重力补偿：大幅上调镁硫比重，保障高密度人工光合作用",
        "调低磷比例，防止微重力吸磷过量引起细胞早衰",
        "太空微重力补偿：大幅上调锰、锌、硼、铜等微量营养素",
        "最高浓度螯合铁补偿，对抗重力缺失下的铁吸收衰竭"
    ]

# 最终所需克数计算
multiplier = target_ec / base_ec_val
weights = {k: v * volume_in_liters * multiplier for k, v in base_calc.items()}

# UI 呈现：分栏显示 A 罐 and B 罐
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🔴 溶液 A 罐 (Tank A - 钙氮罐)")
    st.markdown("将以下成分溶解在适量温水中，搅拌至完全溶解：")
    a_df = pd.DataFrame({
        "化学盐类 (成分)": ["硝酸钙 Ca(NO₃)₂", "硝酸钾 KNO₃"],
        "所需重量 (克)": [f"{weights['Ca(NO3)2']:.2f} g", f"{weights['KNO3']:.2f} g"],
        "配方生理调配说明": explain_a
    })
    st.table(a_df)

with col2:
    st.markdown("### 🔵 溶液 B 罐 (Tank B - 镁磷微量罐)")
    st.markdown("将以下成分溶解在另一个独立容器的温水中：")
    b_df = pd.DataFrame({
        "化学盐类 (成分)": ["硫酸镁 MgSO₄", "磷酸二氢钾 KH₂PO₄ (MKP)", "微量元素混合物", "EDDHA 螯合铁"],
        "所需重量 (克)": [
            f"{weights['MgSO4']:.2f} g",
            f"{weights['KH2PO4']:.2f} g",
            f"{weights['Trace']:.2f} g",
            f"{weights['Fe_EDDHA']:.2f} g"
        ],
        "配方生理调配说明": explain_b
    })
    st.table(b_df)

# ==================== 养分平衡雷达对比图模块 ====================
st.markdown("---")
st.subheader("🕸️ 养分质量占比对比（经典学术 Hoagland 标尺对照）")

# 准备数据
categories = ['硝酸钙 (钙源)', '硝酸钾 (钾氮源)', '硫酸镁 (镁硫源)', '磷酸二氢钾 (磷钾源)', '微量元素', '螯合铁']

# 动态计算当前配方的质量占比
total_base_weight = sum(base_calc.values())
current_pct = [
    (base_calc["Ca(NO3)2"] / total_base_weight) * 100,
    (base_calc["KNO3"] / total_base_weight) * 100,
    (base_calc["MgSO4"] / total_base_weight) * 100,
    (base_calc["KH2PO4"] / total_base_weight) * 100,
    (base_calc["Trace"] / total_base_weight) * 100,
    (base_calc["Fe_EDDHA"] / total_base_weight) * 100,
]

# 学术界 Hoagland No. 2 标准占比 (对照标尺)
hoagland_base = {
    "Ca(NO3)2": 82.0 / 100.0,
    "KNO3": 50.0 / 100.0,
    "MgSO4": 49.0 / 100.0,
    "KH2PO4": 14.0 / 100.0,
    "Trace": 5.0 / 100.0,
    "Fe_EDDHA": 2.5 / 100.0,
}
total_hoagland_weight = sum(hoagland_base.values())
hoagland_pct = [
    (hoagland_base["Ca(NO3)2"] / total_hoagland_weight) * 100,
    (hoagland_base["KNO3"] / total_hoagland_weight) * 100,
    (hoagland_base["MgSO4"] / total_hoagland_weight) * 100,
    (hoagland_base["KH2PO4"] / total_hoagland_weight) * 100,
    (hoagland_base["Trace"] / total_hoagland_weight) * 100,
    (hoagland_base["Fe_EDDHA"] / total_hoagland_weight) * 100,
]

# 分栏显示：左侧是动态雷达图，右侧是极具说服力的专业文字分析
col_chart, col_analysis = st.columns([3, 2])

with col_chart:
    fig = go.Figure()
    
    # 当前配方轮廓
    fig.add_trace(go.Scatterpolar(
        r=current_pct + [current_pct[0]],
        theta=categories + [categories[0]],
        fill='toself',
        name=recipe.split(" - ")[0],
        line_color='#2ca02c',
        fillcolor='rgba(44, 160, 44, 0.35)'
    ))
    
    # 叠加学术经典 Hoagland 2 号作为背景参考
    if "Hoagland" not in recipe:
        fig.add_trace(go.Scatterpolar(
            r=hoagland_pct + [hoagland_pct[0]],
            theta=categories + [categories[0]],
            fill='toself',
            name="Hoagland No. 2 (经典学术基准)",
            line_color='#1f77b4',
            fillcolor='rgba(31, 119, 180, 0.1)',
            line=dict(dash='dash')
        ))
        
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 55],
                ticksuffix="%",
                gridcolor="rgba(128, 128, 128, 0.2)",
                angle=45
            ),
            angularaxis=dict(
                gridcolor="rgba(128, 128, 128, 0.2)"
            )
        ),
        showlegend=True,
        margin=dict(l=50, r=50, t=30, b=30),
        height=400,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col_analysis:
    st.markdown("### 🔍 养分平衡轮廓深度解密")
    
    if "Kratky" in recipe:
        st.markdown("""
        **💡 极简 Kratky 配方特点分析：**
        * **超高占比的微量元素（22.4%）**：由于静止水培中水体不进行流动，养分流动较慢。为了保证植物不会因局部浓度不均而“缺素”，原配方特意提高了微量元素和螯合铁在混合晶体中的比例。
        * **极低占比的磷元素（2.8%）**：生菜等叶菜苗期如果给足磷极易疯狂长根而茎叶空洞。极低磷配比可以让生菜叶盘更紧凑、不徒长。
        """)
    elif "商业级" in recipe:
        st.markdown("""
        **💡 商业级流速高产配方特点分析：**
        * **高度平衡的钙和镁（占 41.4% 和 25.5%）**：流速系统（NFT/垂直塔）中叶片的蒸腾作用极其旺盛，高流速下需要大量的钙、镁来维持叶片挺拔和高密度的光合反应。
        * **经典的低微量元素设计**：由于水体24小时不间断循环，根系接触面极大，因此可以使用更低、更精细的微量元素比例，控制成本，达到高产。
        """)
    elif "Hoagland" in recipe:
        st.markdown("""
        **💡 Hoagland No. 2 经典学术之秤：**
        * **完美的三维平衡**：硝酸钙（40.5%）、硝酸钾（24.7%）、硫酸镁（24.2%）构成了学术界引以为傲的“铁三角”。它是大部分双子叶植物配方的发源母方。
        * 任何配方只要与该轮廓越接近，其全季生长安全指数就越高。您可以以此雷达图作为您自己特调配方的标准指南针。
        """)
    elif "限氮促花" in recipe:
        st.markdown("""
        **💡 限氮促花配方突发性轮廓：**
        * **疯狂扩张的磷钾源（KH₂PO₄ 占比飙升至 18.5%）**：对比 Hoagland 基准，该轮廓往右下方大幅突起。超高的磷钾能刺激植物立刻开启生殖生长、进行丰硕的果实膨大。
        * **收缩的硝酸钙（氮源占 26.5%）**：限氮是挂果后期的核心。通过物理压缩氮素，防止番茄植株枝叶过密，把所有精力留给果实！
        """)
    else:
        st.markdown("""
        **💡 太空模拟微重力配方突起：**
        * **向左侧急剧膨胀的钙（46.6%）与镁（33.9%）**：低重力下，植物因重力缺乏而难以进行正常的阳离子跨膜传输。必须大幅上调钙镁，对抗太空阳离子锁。
        * **极度收缩的硝酸钾与磷酸二氢钾**：在太空中，由于水滴形成和扩散的独特物理学变化，植物吸收游离钾和磷的速率反而发生异常暴涨。必须在配方中物理降准，防单盐中毒、提早早衰。
        """)

# pH 预警模块
st.markdown("---")
st.subheader("⚠️ 实时化学安全与预警")

if water_ph > 6.5:
    st.error(f"🚨 **高 pH 警报 (当前值 {water_ph})**：当 pH 超过 6.5 时，常规铁盐将迅速氧化并产生不溶性沉淀，导致植物无法吸收铁（营养锁定 lockout）。")
    st.markdown("""
    **建议防护措施：**
    1. 确保使用上表计算的 **EDDHA 螯合铁**（比普通 EDTA 铁具有更强的高 pH 耐受性）。
    2. 使用 **柠檬酸** 或 **磷酸 pH 降低剂**，将最终水箱的 pH 精准下调至 **5.8 - 6.2** 之间。
    """)
elif water_ph < 5.5:
    st.warning(f"⚠️ **低 pH 警报 (当前值 {water_ph})**：溶液偏酸性，可能对植物幼嫩的根系产生酸灼伤，并抑制钙、镁的吸收。建议使用氢氧化钾（KOH）进行中和微调。")
else:
    st.success(f"✨ **pH 状态理想 (当前值 {water_ph})**：处于 5.8 - 6.2 的微酸性黄金区间。铁及各常量、微量元素将处于最高溶解度和最佳吸收状态。")

# 流量变现：广告与推荐商品预留位
st.markdown("---")
st.markdown("### 🛒 推荐采购与种植工具（广告 & 佣金变现位）")
ad_col1, ad_col2, ad_col3 = st.columns(3)

with ad_col1:
    st.info("🛒 **高精度电子天平 (0.01g)**")
    st.markdown("[立即在亚马逊采购 ↗](https://example.com/affiliate-scale)  \n*精准称量 A/B 罐微量元素、螯合铁以及克拉茨基微型配方不可或缺的硬件。*")

with ad_col2:
    st.info("🧪 **专业 A/B 双色母液储水罐 (5L)**")
    st.markdown("[查看高赞推荐商家 ↗](https://example.com/affiliate-tanks)  \n*不透光材质，完美防藻、防化学反应沉淀，保证经典配方长久保存。*")

with ad_col3:
    st.info("⚡ **防沉淀 EDDHA 螯合铁 (红色粉末)**")
    st.markdown("[官方联盟直供购买 ↗](https://example.com/affiliate-iron)  \n*攻克黄叶病，学术标准霍格兰或西红柿防脐腐高浓度配方的黄金伴侣。*")

# 实操配制流程
st.markdown("---")
st.subheader("📝 5步标准混溶实操法（防沉淀）")
st.markdown(f"""
1. **分别溶解**：准备两个各装有约总容量 5% 温水（约 40°C）的干净容器，分别完全溶解 **溶液 A 罐** 和 **溶液 B 罐** 的成分。
2. **水箱注水**：在最终的水箱中注入约 80% 的清水。
3. **加入 A 罐并循环**：将完全溶解的 A母液倒入水箱，开启水泵循环搅拌 3-5 分钟。
4. **加入 B 罐并循环**：在 A 罐充分稀释后，缓慢倒入完全溶解的 B 母液，继续加水至最终目标体积 **{volume:.2f} {unit}**，并保持泵循环混匀。
5. **校准测试**：使用 EC 笔测量是否接近目标值 **{target_ec:.1f} mS/cm**；使用 pH 计测试并调整，确保 pH 落在 **5.8 - 6.2** 范围内。
""")
