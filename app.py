import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# 设置页面配置
st.set_page_config(
    page_title="智能水培营养液配方计算器 v6 (中英双语专业版)",
    page_icon="🍀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------- 双语词典 (Bilingual Dictionary) --------------------
TEXTS = {
    "header_title": {
        "中文": "🍀 智能水培营养液配方计算器 (Web v6 - 双语专业版)",
        "English": "🍀 Intelligent Hydroponic Nutrient Calculator (Web v6 - Bilingual Pro Edition)"
    },
    "header_desc": {
        "中文": "通过这套系统，您可以快速计算不同作物在各生长阶段所需的 A/B 母液配比。支持**自来水钙镁背景值自动扣减**等专业级高级功能。",
        "English": "Quickly calculate A/B stock solution ratios for different crops at various growth stages. Features pro-level capabilities such as **automatic tap water calcium and magnesium background deduction**."
    },
    "sidebar_header": {
        "中文": "⚙️ 调配参数设置",
        "English": "⚙️ Configuration Parameters"
    },
    "sel_category": {
        "中文": "1. 选择作物分类",
        "English": "1. Select Crop Category"
    },
    "sel_recipe": {
        "中文": "2. 选择具体生长配方",
        "English": "2. Select Specific Growth Recipe"
    },
    "sel_unit": {
        "中文": "3. 选择水量单位",
        "English": "3. Select Water Unit"
    },
    "sel_volume": {
        "中文": "4. 输入最终稀释总体积",
        "English": "4. Enter Final Diluted Volume"
    },
    "ec_control": {
        "中文": "📈 生长阶段与浓度微调",
        "English": "📈 Growth Stage & EC Fine-Tuning"
    },
    "ec_slider": {
        "中文": "设定目标电导率 (EC, mS/cm)",
        "English": "Set Target Conductivity (EC, mS/cm)"
    },
    "ph_monitor": {
        "中文": "🧪 初始水源 pH 监测",
        "English": "🧪 Source Water pH Monitoring"
    },
    "ph_slider": {
        "中文": "您的水源初始 pH 值",
        "English": "Your Source Water Initial pH"
    },
    "pro_mode": {
        "中文": "🛠️ 专业级功能：自来水背景水质扣减",
        "English": "🛠️ Pro Features: Tap Water Mineral Deduction"
    },
    "pro_enable": {
        "中文": "启用自来水硬度补偿 (扣除已有矿物质)",
        "English": "Enable Tap Water Hardness Compensation"
    },
    "pro_ca_input": {
        "中文": "自来水钙含量 (Ca, PPM)",
        "English": "Tap Water Calcium Level (Ca, PPM)"
    },
    "pro_mg_input": {
        "中文": "自来水镁含量 (Mg, PPM)",
        "English": "Tap Water Magnesium Level (Mg, PPM)"
    },
    "pro_deducted_warning": {
        "中文": "⚠️ **专业硬度补偿提示**：自来水中已含有较高的 {{element}} ({{ppm}} PPM)。配方已自动扣减相应的 {{salt}} **{{deducted}}g**。真实所需称重已更新。",
        "English": "⚠️ **Pro Compensation Notice**: Tap water already contains high {{element}} ({{ppm}} PPM). The recipe has automatically deducted **{{deducted}}g** of {{salt}}. Required weights updated."
    },
    "pro_zero_warning": {
        "中文": "🚨 **元素溢出警告**：自来水中的 {{element}} ({{ppm}} PPM) 已完全超出配方目标！无需额外称重添加 {{salt}}。请注意可能存在的其他盐害风险！",
        "English": "🚨 **Element Excess Warning**: Tap water {{element}} ({{ppm}} PPM) completely exceeds recipe target! NO NEED to add any {{salt}}. Beware of potential salt stress risks!"
    },
    "result_header": {
        "中文": "📊 您专属的配方计算结果",
        "English": "📊 Your Customized Formulation Results"
    },
    "tank_a_title": {
        "中文": "🔴 溶液 A 罐 (Tank A - 钙氮罐)",
        "English": "🔴 Stock Solution Tank A (Calcium & Nitrogen)"
    },
    "tank_a_desc": {
        "中文": "将以下成分溶解在适量温水中，搅拌至完全溶解：",
        "English": "Dissolve the following ingredients in warm water until completely dissolved:"
    },
    "tank_b_title": {
        "中文": "🔵 溶液 B 罐 (Tank B - 镁磷微量罐)",
        "English": "🔵 Stock Solution Tank B (Magnesium & Phosphorus & Traces)"
    },
    "tank_b_desc": {
        "中文": "将以下成分溶解在另一个独立容器的温水中：",
        "English": "Dissolve the following in a separate container of warm water:"
    },
    "tbl_col_salt": {
        "中文": "化学盐类 (成分)",
        "English": "Chemical Salt / Compound"
    },
    "tbl_col_weight": {
        "中文": "所需重量 (克)",
        "English": "Required Weight (g)"
    },
    "tbl_col_desc": {
        "中文": "配方生理调配说明",
        "English": "Physiological & Batching Notes"
    },
    "ph_alert_high": {
        "中文": "🚨 **高 pH 警报 (当前值 {{ph}})**：当 pH 超过 6.5 时，常规铁盐将迅速氧化并产生不溶性沉淀，导致植物无法吸收铁（营养锁定 lockout）。\n\n**建议防护措施：**\n1. 确保使用上表计算的 **EDDHA 螯合铁**（比普通 EDTA 铁具有更强的高 pH 耐受性）。\n2. 使用 **柠檬酸** 或 **磷酸 pH 降低剂**，将最终水箱的 pH 精准下调至 **5.8 - 6.2** 之间。",
        "English": "🚨 **High pH Alert (Current: {{ph}})**: When pH exceeds 6.5, standard iron salts oxidize rapidly and form insoluble precipitation, resulting in iron nutrient lockout.\n\n**Recommended Remedies:**\n1. Ensure you use **EDDHA Chelated Iron** as calculated above (much more stable at high pH than EDTA-Fe).\n2. Use **Citric Acid** or **Phosphoric Acid (pH Down)** to adjust the reservoir pH to the golden range of **5.8 - 6.2**."
    },
    "ph_alert_low": {
        "中文": "⚠️ **低 pH 警报 (当前值 {{ph}})**：溶液偏酸性，可能对植物幼嫩的根系产生酸灼伤，并抑制钙、镁的吸收。建议使用氢氧化钾（KOH）进行中和微调。",
        "English": "⚠️ **Low pH Alert (Current: {{ph}})**: The solution is too acidic, which can cause chemical root burns and suppress the absorption of Calcium and Magnesium. Adjust upwards using Potassium Hydroxide (KOH)."
    },
    "ph_alert_ok": {
        "中文": "✨ **pH 状态理想 (当前值 {{ph}})**：处于 5.8 - 6.2 的微酸性黄金区间。铁及各常量、微量元素将处于最高溶解度和最佳吸收状态。",
        "English": "✨ **Ideal pH Status (Current: {{ph}})**: Perfect微酸性 golden range (5.8 - 6.2). Iron and all macronutrients/micronutrients are at peak solubility and bioavailability."
    },
    "radar_title": {
        "中文": "🕸️ 养分质量占比对比（经典学术 Hoagland 标尺对照）",
        "English": "🕸️ Nutrient Mass Balance Profile (VS. Classic Hoagland No. 2)"
    },
    "radar_desc_title": {
        "中文": "🔍 养分平衡轮廓深度解密",
        "English": "🔍 Nutrient Balance Profile Decoded"
    },
    "affiliate_title": {
        "中文": "📬 加入极客群聊与订阅",
        "English": "📬 Join Our Community & Newsletter"
    },
    "ad1_title": {
        "中文": "✉️ 订阅每周配方",
        "English": "✉️ Weekly Formulas"
    },
    "ad1_desc": {
        "中文": "想要草莓、罗勒的特调配方？订阅我们的免费邮件周报！\n\n👉 [立即订阅](mailto:judezy89@gmail.com?subject=Subscribe%20Hydroponics)",
        "English": "Want custom formulas for strawberries or basil? Subscribe to our newsletter!\n\n👉 [Subscribe via Email](mailto:your_email@gmail.com?subject=Subscribe%20Hydroponics)"
    },
    "ad2_title": {
        "中文": "💬 微信极客交流群",
        "English": "💬 WeChat Community"
    },
    "ad2_desc": {
        "中文": "加入千人水培大群，与全球种植大咖面对面交流。\n\n👉 **微信号: kslab01ID** (备注: 水培)",
        "English": "Join 1000+ growers in our private community.\n\n👉 **Add WeChat: kslab01** (Note: Hydro)"
    },
    "ad3_title": {
        "中文": "👾 Discord & Reddit",
        "English": "👾 Discord & Reddit"
    },
    "ad3_desc": {
        "中文": "加入全球 Discord 社区，提交您的特调雷达图。\n\n👉 [进入社区](https://discord.gg/your_link)",
        "English": "Connect with worldwide growers on our Discord!\n\n👉 [Join Discord](https://discord.gg/your_link)"
    },
    "instructions_title": {
        "中文": "📝 5步标准混溶实操法（防沉淀）",
        "English": "📝 5-Step Scientific Mixing Method (Anti-Precipitation)"
    },
    "instructions_steps": {
        "中文": """
1. **分别溶解**：准备两个各装有约总容量 5% 温水（约 40°C）的干净容器，分别完全溶解 **溶液 A 罐** 和 **溶液 B 罐** 的成分。
2. **水箱注水**：在最终的水箱中注入约 80% 的清水。
3. **加入 A 罐并循环**：将完全溶解的 A 母液倒入水箱，开启水泵循环搅拌 3-5 分钟。
4. **加入 B 罐并循环**：在 A 罐充分稀释后，缓慢倒入完全溶解的 B 母液，继续加水至最终目标体积 **{volume:.2f} {unit}**，并保持泵循环混匀。
5. **校准测试**：使用 EC 笔测量是否接近目标值 **{target_ec:.1f} mS/cm**；使用 pH 计测试并调整，确保 pH 落在 **5.8 - 6.2** 范围内。
""",
        "English": """
1. **Separate Dissolution**: Prepare two separate containers containing ~5% of final volume warm water (~40°C). Completely dissolve **Tank A** and **Tank B** powders separately.
2. **Fill Main Reservoir**: Fill your final water reservoir with ~80% of target clean water.
3. **Add Tank A & Circulate**: Pour the dissolved Tank A stock solution into the reservoir. Turn on the pump to circulate and mix for 3-5 minutes.
4. **Add Tank B & Dilute**: Once Tank A is fully diluted, slowly pour in dissolved Tank B. Top off with water until final target volume of **{volume:.2f} {unit}** is reached, and mix thoroughly.
5. **Calibrate & Adjust**: Check the final EC with a conductivity meter to confirm it is close to **{target_ec:.1f} mS/cm**. Measure and adjust pH using pH Up/Down until it stabilizes in the **5.8 - 6.2** range.
"""
    }
}

# -------------------- 侧边栏语言选择 (Sidebar Language Select) --------------------
lang = st.sidebar.selectbox("🌐 Language / 选择语言", ["English", "中文"])

def translate(key):
    return TEXTS[key][lang]

# -------------------- 网站标题与介绍 --------------------
st.title(translate("header_title"))
st.markdown(translate("header_desc"))

# 侧边栏：核心配置
st.sidebar.header(translate("sidebar_header"))

# 1. 作物分类
categories_list = {
    "中文": ["生菜 (Lettuce) - 绿叶菜黄金通道", "西红柿 (Tomato) - 挂果高值通道", "黄瓜 (Cucumber) - 高产NFT循环通道", "太空模拟 (Space Farms) - 极客引流卖点"],
    "English": ["Lettuce - Leafy Green Channels", "Tomato - Fruiting High-Value Channels", "Cucumber - High-Yield NFT Channels", "Space Farms - Space Simulation Geek Channels"]
}
crop_category = st.sidebar.selectbox(translate("sel_category"), categories_list[lang])

# 2. 生长配方
recipes_map = {
    "生菜 (Lettuce) - 绿叶菜黄金通道": [
        "生菜 - Kratky 极简免维护配方 (最适合阳台新手)",
        "生菜 - 商业级 NFT/垂直塔高产高氮配方 (促叶生长期)"
    ],
    "Lettuce - Leafy Green Channels": [
        "Lettuce - Kratky Low-Maintenance Formula (Best for Balcony Newbies)",
        "Lettuce - Commercial NFT/Tower High-Yield Formula (Vegetative Stage)"
    ],
    "黄瓜 (Cucumber) - 高产NFT循环通道": [
        "黄瓜 - NFT闭合循环高产配方 (1000L系统验证)"
    ],
    "Cucumber - High-Yield NFT Channels": [
        "Cucumber - NFT Closed-Loop High-Yield Formula (1000L Field-Tested)"
    ],
    "西红柿 (Tomato) - 挂果高值通道": [
        "西红柿 - Hoagland No. 2 学术级黄金平衡配方",
        "西红柿 - 挂果中后期“限氮促花”强效配方 (防脐腐病)"
    ],
    "Tomato - Fruiting High-Value Channels": [
        "Tomato - Hoagland No. 2 Academic Gold Standard Formula",
        "Tomato - Fruiting Stage 'Low-Nitrogen Heavy-K' Formula (BER Prevention)"
    ],
    "太空模拟 (Space Farms) - 极客引流卖点": [
        "太空模拟豌豆 - Microgravity Sim 🌌 (NASA低重力调配)"
    ],
    "Space Farms - Space Simulation Geek Channels": [
        "Space Peas - Microgravity Sim 🌌 (NASA Low-Gravity Adjustment)"
    ]
}
recipe = st.sidebar.selectbox(translate("sel_recipe"), recipes_map[crop_category])

# 3. 水量与单位
unit_labels = {"中文": ["升 (L)", "加仑 (GAL)"], "English": ["Liters (L)", "Gallons (GAL)"]}
unit = st.sidebar.radio(translate("sel_unit"), unit_labels[lang], index=0)
volume = st.sidebar.number_input(translate("sel_volume"), min_value=1.0, value=100.0, step=10.0)

# 统一换算为升进行计算 (1 Gallon = 3.78541 Liters)
volume_in_liters = volume if ("升" in unit or "Liters" in unit) else volume * 3.78541

# 4. 目标 EC 调节
st.sidebar.markdown("---")
st.sidebar.subheader(translate("ec_control"))

# 根据所选配方设定默认 EC
if "Kratky" in recipe:
    default_ec, min_ec, max_ec = 1.4, 0.8, 1.8
    info_text = {
        "中文": "💡 Kratky 极简配方推荐 EC：1.2 - 1.6 mS/cm。该方法无需气泵，适合静止水培。",
        "English": "💡 Kratky method recommends EC: 1.2 - 1.6 mS/cm. Requires no water pumps; ideal for passive hydroponics."
    }
elif "商业级" in recipe or "Commercial" in recipe:
    default_ec, min_ec, max_ec = 1.5, 1.0, 2.0
    info_text = {
        "中文": "💡 商业 NFT 循环系统需要较高氮肥，推荐 EC：1.4 - 1.8 mS/cm，促进叶片快速膨大。",
        "English": "💡 Commercial active systems need high nitrate. Recommended EC: 1.4 - 1.8 mS/cm for accelerated vegetative growth."
    }
elif "黄瓜" in recipe or "Cucumber" in recipe:
    default_ec, min_ec, max_ec = 2.0, 1.2, 2.5
    info_text = {
        "中文": "💡 黄瓜NFT系统推荐 EC：1.8 - 2.2 mS/cm。高流动大水体有助于根系充分吸收钙钾。",
        "English": "💡 Cucumber NFT closed system recommends EC: 1.8 - 2.2 mS/cm. Dynamic flow aids rapid calcium and potassium mass transport."
    }
elif "Hoagland" in recipe:
    default_ec, min_ec, max_ec = 2.0, 1.5, 2.5
    info_text = {
        "中文": "💡 霍格兰二号是学术界黄金标尺。全阶段平衡配方，推荐 EC：1.8 - 2.2 mS/cm。",
        "English": "💡 Hoagland No. 2 is the universal academic benchmark. Balanced formula. Recommended EC: 1.8 - 2.2 mS/cm."
    }
elif "限氮促花" in recipe or "Fruiting Stage" in recipe:
    default_ec, min_ec, max_ec = 2.2, 1.8, 2.8
    info_text = {
        "中文": "💡 挂果期大幅度提高磷钾、限制氮源以促进果实发育，高 EC：2.0 - 2.5 mS/cm，可有效防止脐腐病。",
        "English": "💡 Late fruiting boosts P and K while limiting nitrogen to prompt massive fruit sizing. High EC: 2.0 - 2.5 mS/cm prevents Blossom End Rot."
    }
else:
    default_ec, min_ec, max_ec = 1.8, 1.2, 2.4
    info_text = {
        "中文": "🛸 太空微重力下二价阳离子（钙镁铁）吸收受阻，而单价阴阳离子（磷钾）吸收异常激增。推荐 EC：1.6 - 2.0 mS/cm。",
        "English": "🛸 Microgravity hampers divalent cation (Ca/Mg/Fe) absorption but spikes monovalent ions (P/K). Recommended EC: 1.6 - 2.0 mS/cm."
    }

st.sidebar.info(info_text[lang])
target_ec = st.sidebar.slider(translate("ec_slider"), min_value=min_ec, max_value=max_ec, value=default_ec, step=0.1)

# 5. pH 监测
st.sidebar.markdown("---")
st.sidebar.subheader(translate("ph_monitor"))
water_ph = st.sidebar.slider(translate("ph_slider"), min_value=4.0, max_value=8.5, value=6.5, step=0.1)

# 6. 专业硬度扣除
st.sidebar.markdown("---")
st.sidebar.subheader(translate("pro_mode"))
pro_enabled = st.sidebar.checkbox(translate("pro_enable"), value=False)
tap_ca = 0.0
tap_mg = 0.0
if pro_enabled:
    tap_ca = st.sidebar.number_input(translate("pro_ca_input"), min_value=0.0, value=40.0, step=5.0)
    tap_mg = st.sidebar.number_input(translate("pro_mg_input"), min_value=0.0, value=12.0, step=2.0)


# -------------------- 核心配方克数计算 --------------------
# 基础配方数据（基于100L水和各自的基准 EC）
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
    explain_a_map = {
        "中文": ["提供植株骨架发育的钙源（100% 硝态氮）", "Kratky 系统中温和、不烧根的高效钾氮源"],
        "English": ["Provides calcium for plant cell walls (100% nitrate nitrogen)", "Gentle, non-burning potassium source ideal for passive reservoirs"]
    }
    explain_b_map = {
        "中文": [
            "维持静止水培下叶片叶绿素合成",
            "极低剂量磷源，防止前期疯狂徒长，保证根系舒展",
            "提供微量元素补充，防止黄化",
            "螯合铁防止静止营养液高 pH 沉淀 lockout"
        ],
        "English": [
            "Maintains chlorophyll synthesis in passive water conditions",
            "Minimal phosphorus to prevent early vegetative leggy stretch while letting roots spread",
            "Provides balanced trace elements to bypass micro-deficiencies",
            "EDDHA iron prevents nutrient lockout in alkaline water or high-pH stagnation"
        ]
    }
elif "商业级" in recipe or "Commercial" in recipe:
    base_calc = {
        "Ca(NO3)2": 65.0 / 100.0,
        "KNO3": 30.0 / 100.0,
        "MgSO4": 40.0 / 100.0,
        "KH2PO4": 15.0 / 100.0,
        "Trace": 5.0 / 100.0,
        "Fe_EDDHA": 2.0 / 100.0,
    }
    base_ec_val = 1.4
    explain_a_map = {
        "中文": ["商业 NFT 高产的高效硝态氮，促进叶绿素积累", "超高溶解度钾源，在水流循环中为茎叶极速泵送养分"],
        "English": ["Highly efficient nitrate nitrogen for fast vegetative cell multiplication", "Highly soluble potassium to accelerate transport systems in active water loops"]
    }
    explain_b_map = {
        "中文": [
            "支持强光照垂直塔系统下的镁硫高消耗",
            "提供充足的磷源，促进快速分蘖与多叶叶盘形成",
            "高度适配流速系统的微量元素补充",
            "螯合铁防止营养液频繁流动与空气接触导致的氧化沉淀"
        ],
        "English": [
            "Sustains high magnesium consumption in high-intensity light towers",
            "Ample phosphorus for rapid multi-crown development and massive leaf expansion",
            "Optimized micro-dose traces matching high-flow plant consumption rates",
            "EDDHA iron resists oxidation caused by continuous air contact and pump agitation"
        ]
    }
elif "黄瓜" in recipe or "Cucumber" in recipe:
    base_calc = {
        "Ca(NO3)2": 80.0 / 100.0,
        "KNO3": 40.0 / 100.0,
        "MgSO4": 60.0 / 100.0,
        "KH2PO4": 20.0 / 100.0,
        "Trace": 5.0 / 100.0,
        "Fe_EDDHA": 1.5 / 100.0,
    }
    base_ec_val = 2.0
    explain_a_map = {
        "中文": ["提供黄瓜果实生长所需核心氮钙比例", "促进主茎伸长与早期挂果高能钾素"],
        "English": ["Provides optimal nitrogen-to-calcium ratio for heavy cucumber vine structures", "Powers stem elongation and rapid potassium loading in early fruit sets"]
    }
    explain_b_map = {
        "中文": [
            "提供果实膨大期的硫、镁元素平衡",
            "促根、壮苗与花芽分化的基础磷钾源 (MKP)",
            "补偿NFT循环中高消耗微量元素",
            "强效螯合铁，彻底解决密闭管道根系缺铁黄化问题"
        ],
        "English": [
            "Maintains magnesium and sulfur equilibrium for active leaf canopy photosynthesis",
            "Premium soluble phosphorus-potassium source (MKP) for flowering and robust rooting",
            "Replenishes micro-dose trace elements consumed rapidly in closed NFT loops",
            "Superior chelated EDDHA-Fe halts iron chlorosis in high-transpiration PVC gullies"
        ]
    }
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
    explain_a_map = {
        "中文": ["学术界番茄防脐腐病的标准钙水平 (约 150-200 ppm)", "平衡生长全阶段所需的标准钾与硝态氮比例"],
        "English": ["Academic gold standard calcium level (150-200 ppm Ca) to defeat Blossom End Rot", "Standard nitrogen-to-potassium balance for steady all-season development"]
    }
    explain_b_map = {
        "中文": [
            "提供稳定的镁源，防止老叶叶脉间缺镁黄化",
            "经典 31 ppm 磷酸盐水平，维持健康的根系与细胞分裂",
            "提供经典的霍格兰无机微量元素群",
            "高稳定性螯合铁，确保光合作用最高效能"
        ],
        "English": [
            "Stable magnesium prevents interveinal chlorosis in older lower leaves",
            "Classic 31 ppm phosphorus level supports sturdy root structures and energy cycles",
            "Comprehensive Hoagland micro-nutrient mineral cocktail",
            "Premium stable EDDHA chelate protects iron from high-pH precipitation lock"
        ]
    }
elif "限氮促花" in recipe or "Fruiting Stage" in recipe:
    base_calc = {
        "Ca(NO3)2": 50.0 / 100.0,
        "KNO3": 45.0 / 100.0,
        "MgSO4": 50.0 / 100.0,
        "KH2PO4": 35.0 / 100.0,
        "Trace": 6.0 / 100.0,
        "Fe_EDDHA": 3.0 / 100.0,
    }
    base_ec_val = 2.2
    explain_a_map = {
        "中文": ["适度限氮，防止西红柿挂果后期枝叶疯长、营养徒长", "高水平钾元素，强效膨果，增加番茄红素与干物质积累"],
        "English": ["Limits nitrogen strictly to stop vegetative over-growth and redirect energy to fruits", "Extreme potassium for heavy fruit sizing, boosting lycopene and brix (sugar) density"]
    }
    explain_b_map = {
        "中文": [
            "保障高产挂果期的叶片能量代谢",
            "超高磷配比，强效诱导花芽分化，实现极致的果实饱满度",
            "挂果期高消耗微量元素补偿",
            "螯合铁防沉淀高强度升级，保障高蒸腾作用下的叶绿素密度"
        ],
        "English": [
            "Sustains leaf metabolic energy during heavy reproductive loads",
            "Super-charged phosphorus forces flower differentiation and maximizes fruit count",
            "Replenishes high-consumption micronutrients drawn during fruit ripening",
            "Maximized EDDHA-Fe prevents iron depletion under intense hot-house transpiration"
        ]
    }
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
    explain_a_map = {
        "中文": ["太空微重力吸收效率降低，大幅上调钙源补偿植株骨架", "调低钾比例，防止微重力极速高吸收引起的钾中毒"],
        "English": ["Boosts calcium dramatically to bypass divalent cation transport barriers in microgravity", "Slashes potassium to prevent rapid hyper-accumulation toxicity in low gravity"]
    }
    explain_b_map = {
        "中文": [
            "太空低重力补偿：大幅上调镁硫比重，保障高密度人工光合作用",
            "调低磷比例，防止微重力吸磷过量引起细胞早衰",
            "太空微重力补偿：大幅上调锰、锌、硼、铜等微量营养素",
            "最高浓度螯合铁补偿，对抗重力缺失下的铁吸收衰竭"
        ],
        "English": [
            "Microgravity compensation: boosts magnesium/sulfur to fuel closed-environment photosynthesis",
            "Slashes phosphorus to prevent rapid uptake leading to premature plant senescence",
            "Microgravity compensation: heavily enriches manganese, zinc, boron, and copper",
            "Double-strength chelate offsets weak mineral transpiration in microgravity environments"
        ]
    }

# 最终所需克数计算 (基本等比缩放)
multiplier = target_ec / base_ec_val
raw_weights = {k: v * volume_in_liters * multiplier for k, v in base_calc.items()}

# 专业硬度扣除数学转化逻辑 (Pro Tap Water Deduction Mathematics)
# 1 ppm Ca = 5.89 mg/L Calcium Nitrate Tetrahydrate (Ca(NO3)2·4H2O) -> 0.00589 g/L
# 1 ppm Mg = 10.14 mg/L Epsom Salt (MgSO4·7H2O) -> 0.01014 g/L
ca_deduction = 0.0
mg_deduction = 0.0
ca_is_zero = False
mg_is_zero = False

if pro_enabled:
    ca_deduction = tap_ca * 0.00589 * volume_in_liters
    mg_deduction = tap_mg * 0.01014 * volume_in_liters

# 复制最终称重字典并进行扣除
final_weights = raw_weights.copy()

if pro_enabled:
    # 钙源扣除
    if ca_deduction >= raw_weights["Ca(NO3)2"]:
        final_weights["Ca(NO3)2"] = 0.0
        ca_is_zero = True
    else:
        final_weights["Ca(NO3)2"] = raw_weights["Ca(NO3)2"] - ca_deduction
    
    # 镁源扣除
    if mg_deduction >= raw_weights["MgSO4"]:
        final_weights["MgSO4"] = 0.0
        mg_is_zero = True
    else:
        final_weights["MgSO4"] = raw_weights["MgSO4"] - mg_deduction

# 开始生成网页前端展示
st.subheader(translate("result_header"))

# 若开启专业版，输出扣除警报
if pro_enabled:
    if ca_deduction > 0:
        if ca_is_zero:
            msg = translate("pro_zero_warning").replace("{{element}}", "Calcium (Ca)").replace("{{ppm}}", f"{tap_ca:.1f}").replace("{{salt}}", "Ca(NO₃)₂")
            st.warning(msg)
        else:
            msg = translate("pro_deducted_warning").replace("{{element}}", "Calcium (Ca)").replace("{{ppm}}", f"{tap_ca:.1f}").replace("{{salt}}", "Ca(NO₃)₂").replace("{{deducted}}", f"{ca_deduction:.2f}")
            st.info(msg)
            
    if mg_deduction > 0:
        if mg_is_zero:
            msg = translate("pro_zero_warning").replace("{{element}}", "Magnesium (Mg)").replace("{{ppm}}", f"{tap_mg:.1f}").replace("{{salt}}", "MgSO₄")
            st.warning(msg)
        else:
            msg = translate("pro_deducted_warning").replace("{{element}}", "Magnesium (Mg)").replace("{{ppm}}", f"{tap_mg:.1f}").replace("{{salt}}", "MgSO₄").replace("{{deducted}}", f"{mg_deduction:.2f}")
            st.info(msg)

# UI：分栏显示 A、B 罐
col1, col2 = st.columns(2)

with col1:
    st.markdown(f"### {translate('tank_a_title')}")
    st.markdown(translate('tank_a_desc'))
    a_df = pd.DataFrame({
        translate("tbl_col_salt"): ["硝酸钙 Ca(NO₃)₂", "硝酸钾 KNO₃"],
        translate("tbl_col_weight"): [f"{final_weights['Ca(NO3)2']:.2f} g", f"{final_weights['KNO3']:.2f} g"],
        translate("tbl_col_desc"): explain_a_map[lang]
    })
    st.table(a_df)

with col2:
    st.markdown(f"### {translate('tank_b_title')}")
    st.markdown(translate('b_df_desc' if 'b_df_desc' in TEXTS else 'tank_b_desc'))
    b_df = pd.DataFrame({
        translate("tbl_col_salt"): ["硫酸镁 MgSO₄", "磷酸二氢钾 KH₂PO₄ (MKP)", "微量元素混合物", "EDDHA 螯合铁"],
        translate("tbl_col_weight"): [
            f"{final_weights['MgSO4']:.2f} g",
            f"{final_weights['KH2PO4']:.2f} g",
            f"{final_weights['Trace']:.2f} g",
            f"{final_weights['Fe_EDDHA']:.2f} g"
        ],
        translate("tbl_col_desc"): explain_b_map[lang]
    })
    st.table(b_df)

# pH 预警模块
st.markdown("---")
st.subheader("⚠️ pH Alert" if lang == "English" else "⚠️ 实时化学安全与预警")

if water_ph > 6.5:
    alert_txt = translate("ph_alert_high").replace("{{ph}}", f"{water_ph:.1f}")
    st.error(alert_txt)
elif water_ph < 5.5:
    alert_txt = translate("ph_alert_low").replace("{{ph}}", f"{water_ph:.1f}")
    st.warning(alert_txt)
else:
    alert_txt = translate("ph_alert_ok").replace("{{ph}}", f"{water_ph:.1f}")
    st.success(alert_txt)

# -------------------- 动态 Plotly 养分雷达对照图 --------------------
st.markdown("---")
st.subheader(translate("radar_title"))

categories = ['硝酸钙 (Ca)', '硝酸钾 (K)', '硫酸镁 (Mg)', '磷酸二氢钾 (P)', '微量元素 (Trace)', '螯合铁 (Fe)']
if lang == "English":
    categories = ['Calcium Nitrate (Ca)', 'Potassium Nitrate (K)', 'Magnesium Sulfate (Mg)', 'Monopotassium Phosphate (P)', 'Trace Elements', 'Chelated Iron (Fe)']

# 当前配方比例
total_raw_weight = sum(raw_weights.values())
current_pct = [
    (raw_weights["Ca(NO3)2"] / total_raw_weight) * 100,
    (raw_weights["KNO3"] / total_raw_weight) * 100,
    (raw_weights["MgSO4"] / total_raw_weight) * 100,
    (raw_weights["KH2PO4"] / total_raw_weight) * 100,
    (raw_weights["Trace"] / total_raw_weight) * 100,
    (raw_weights["Fe_EDDHA"] / total_raw_weight) * 100,
]

# Hoagland No. 2 标准
hoagland_base = {
    "Ca(NO3)2": 82.0 / 100.0,
    "KNO3": 50.0 / 100.0,
    "MgSO4": 49.0 / 100.0,
    "KH2PO4": 14.0 / 100.0,
    "Trace": 5.0 / 100.0,
    "Fe_EDDHA": 2.5 / 100.0,
}
total_hoagland = sum(hoagland_base.values())
hoagland_pct = [
    (hoagland_base["Ca(NO3)2"] / total_hoagland) * 100,
    (hoagland_base["KNO3"] / total_hoagland) * 100,
    (hoagland_base["MgSO4"] / total_hoagland) * 100,
    (hoagland_base["KH2PO4"] / total_hoagland) * 100,
    (hoagland_base["Trace"] / total_hoagland) * 100,
    (hoagland_base["Fe_EDDHA"] / total_hoagland) * 100,
]

col_chart, col_analysis = st.columns([3, 2])

with col_chart:
    fig = go.Figure()
    # 当前配方
    fig.add_trace(go.Scatterpolar(
        r=current_pct + [current_pct[0]],
        theta=categories + [categories[0]],
        fill='toself',
        name="Selected Recipe" if lang == "English" else "当前选中配方",
        line_color='#2ca02c',
        fillcolor='rgba(44, 160, 44, 0.35)'
    ))
    # 叠加 Hoagland 参考
    if "Hoagland" not in recipe:
        fig.add_trace(go.Scatterpolar(
            r=hoagland_pct + [hoagland_pct[0]],
            theta=categories + [categories[0]],
            fill='toself',
            name="Hoagland No. 2 Benchmark",
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
            angularaxis=dict(gridcolor="rgba(128, 128, 128, 0.2)")
        ),
        showlegend=True,
        margin=dict(l=50, r=50, t=30, b=30),
        height=400,
        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
    )
    st.plotly_chart(fig, use_container_width=True)

with col_analysis:
    st.markdown(f"### {translate('radar_desc_title')}")
    if "Kratky" in recipe:
        if lang == "English":
            st.markdown("""
            **💡 Passive Kratky Profile Analysis:**
            * **High Micronutrients (22.4%)**: Stagnant solution locks down mineral convection. Higher micro-mix buffers the stagnant boundary layers on roots to prevent long-term trace deficiencies.
            * **Low Phosphorus (2.8%)**: Suppresses early shoot stretching, allowing steady root-zone development before full water drop.
            """)
        else:
            st.markdown("""
            **💡 极简 Kratky 配方特点分析：**
            * **超高占比的微量元素（22.4%）**：由于静止水培中水体不进行流动，养分流动较慢。为了保证植物不会因局部浓度不均而“缺素”，原配方特意提高了微量元素和螯合铁在混合晶体中的比例。
            * **极低占比的磷元素（2.8%）**：生菜等叶菜苗期如果给足磷极易疯狂长根而物极必反。极低磷配比可以让生菜叶盘更紧凑、不徒长。
            """)
    elif "商业级" in recipe or "Commercial" in recipe:
        if lang == "English":
            st.markdown("""
            **💡 Commercial NFT Active Profile Analysis:**
            * **Strong Divalent Cation Focus (Ca 41.4%, Mg 25.5%)**: Continuous high transpiration under sun/grow-lights requires solid calcium/magnesium delivery for cell-wall turgor and chlorophyll production.
            * **Micro-efficiency**: Relies on mass flow in the water loop; trace levels can be minimized to save fertilizer costs in commercial runs.
            """)
        else:
            st.markdown("""
            **💡 商业级流速高产配方特点分析：**
            * **高度平衡的钙和镁（占 41.4% 和 25.5%）**：流速系统（NFT/垂直塔）中叶片的蒸腾作用极其旺盛，高流速下需要大量的钙、镁来维持叶片挺拔和高密度的光合反应。
            * **经典的低微量元素设计**：由于水体24小时不间断循环，根系接触面极大，因此可以使用更低、更精细的微量元素比例，控制成本，达到高产。
            """)
    elif "黄瓜" in recipe or "Cucumber" in recipe:
        if lang == "English":
            st.markdown("""
            **💡 Cucumber NFT Closed-Loop Profile Analysis:**
            * **High Magnesium & Sulfur (30.0%)**: Cucumber vines have large leaf areas and high transpiration, requiring elevated magnesium for heavy chlorophyll production.
            * **Well-Balanced Potassium (20.0%)**: Supports robust stem elongation and heavy fruit sizing during active vegetative and reproductive cycles.
            """)
        else:
            st.markdown("""
            **💡 黄瓜 NFT 闭合循环配方特点分析：**
            * **极高占比的硫与镁（占 30.0%）**：黄瓜属于阔叶高蒸腾作物，高含量的镁和硫是支撑其大叶片叶绿素合成与主茎持续拉长、开花的生命支柱。
            * **温和稳定的钾含量（20.0%）**：确保黄瓜在挂果期间得到稳定的养分充盈，防藤蔓早衰。
            """)
    elif "Hoagland" in recipe:
        if lang == "English":
            st.markdown("""
            **💡 Hoagland No. 2 Academic Equilibrium:**
            * **Universal Balance**: The legendary ratios of Ca (40.5%), K (24.7%), and Mg (24.2%) form the absolute chemical triangle of plant nutrition.
            * Ideal benchmark for analyzing custom formulas. Deviation tells you what has been boosted or suppressed.
            """)
        else:
            st.markdown("""
            **💡 Hoagland No. 2 经典学术之秤：**
            * **完美的三维平衡**：硝酸钙（40.5%）、硝酸钾（24.7%）、硫酸镁（24.2%）构成了学术界引以为傲的“铁三角”。它是大部分双子叶植物配方的发源母方。
            * 任何配方只要与该轮廓越接近，其全季生长安全指数就越高。您可以以此雷达图作为您自己特调配方的标准指南针。
            """)
    elif "限氮促花" in recipe or "Fruiting Stage" in recipe:
        if lang == "English":
            st.markdown("""
            **💡 Generative Stage 'Low-Nitrogen Heavy-K' Profile:**
            * **Massive P/K Expansion (KH₂PO₄ spikes to 18.5%)**: Shakes the vegetative cycle. Heavy phosphorus and potassium redirect plant metabolic pathways to trigger dense blossoms.
            * **Suppressed Calcium Nitrate (N cut to 26.5%)**: Prevents excessive leafy canopy growth, sending raw sugars directly to swelling fruits. Prevents Blossom End Rot.
            """)
        else:
            st.markdown("""
            **💡 限氮促花配方突发性轮廓：**
            * **疯狂扩张的磷钾源（KH₂PO₄ 占比飙升至 18.5%）**：对比 Hoagland 基准，该轮廓往右下方大幅突起。超高的磷钾能刺激植物立刻开启生殖生长、进行丰硕的果实膨大。
            * **收缩的硝酸钙（氮源占 26.5%）**：限氮是挂果后期的核心。通过物理压缩氮素，防止番茄植株枝叶过密，把所有精力留给果实！
            """)
    else:
        if lang == "English":
            st.markdown("""
            **💡 Spaceflight Microgravity Simulator Profile:**
            * **Divalent Cation Explosion (Ca 46.6%, Mg 33.9%)**: Overcomes severe biological blockages of Calcium, Magnesium, and Iron membrane transport under zero-gravity conditions.
            * **Suppressed Potassium/Phosphorus**: Low gravity accelerates passive P/K accumulation, risking ion toxicity. Slashed in formulation to maintain cellular balance.
            """)
        else:
            st.markdown("""
            **💡 太空模拟微重力配方突起：**
            * **向左侧急剧膨胀的钙（46.6%）与镁（33.9%）**：低重力下，植物因重力缺乏而难以进行正常的阳离子跨膜传输。必须大幅上调钙镁，对抗太空阳离子锁。
            * **极度收缩的硝酸钾与磷酸二氢钾**：在太空中，由于水滴形成和扩散的独特物理学变化，植物吸收游离钾和磷的速率反而发生异常暴涨。必须在配方中物理降准，防单盐中毒、提早早衰。
            """)

# 变现区域
st.markdown("---")
st.subheader(translate("affiliate_title"))
ad_col1, ad_col2, ad_col3 = st.columns(3)

with ad_col1:
    st.info(translate("ad1_title"))
    st.markdown(translate("ad1_desc"))

with ad_col2:
    st.info(translate("ad2_title"))
    st.markdown(translate("ad2_desc"))

with ad_col3:
    st.info(translate("ad3_title"))
    st.markdown(translate("ad3_desc"))

# 混溶步骤
st.markdown("---")
st.subheader(translate("instructions_title"))
st.markdown(translate("instructions_steps").format(volume=volume, unit=unit, target_ec=target_ec))
