# 🌱 智能水培营养液配方计算器与分析仪 (Hydroponic Stock Solution & Nutrient Balance Analyzer)

[![Streamlit App](https://static.streamlit.io/badge_svg.svg)](https://share.streamlit.io/)
[![Python Version](https://img.shields.io/badge/python-3.12-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

一个专门为水培植物爱好者、商业种植者和极客玩家打造的**全功能在线营养液配方计算与分析平台**。

本工具基于经典水培营养学著作（J. Benton Jones Jr. 经典理论）与前沿空间植物生理学研究（NASA 空间站微重力培养数据），提供动态配方缩放、A/B罐防沉淀混溶工艺指导、实时 pH 化学安全性预警，以及独创的**动态养分平衡雷达对照图**。

---

## ✨ 核心亮点功能

### 1. 🥬 黄金引流作物矩阵与经典配方库
内置多套经过科学验证、高度优化的“明星作物”与经典学术配方：
*   **生菜 - Kratky 极简免维护配方**：都市阳台新手入门黄金配方，主打“零电力、零气泵、一次加水静置到收割”。
*   **生菜 - 商业级 NFT/垂直塔高产高氮配方**：针对循环流速水培系统，极速积累生物质。
*   **西红柿 - Hoagland No. 2 学术级黄金平衡配方**：水培学术界的“通用真理”，完美的微量与大量元素配比标尺。
*   **西红柿 - 挂果中后期“限氮促花”强效配方**：精准限制铵态氮比例，大幅拉升磷钾、稳定钙水平，**从根本上预防西红柿脐腐病（Blossom-End Rot）并防止后期徒长**。
*   **太空模拟豌豆 - Microgravity Sim (NASA微重力调配) 🌌**：根据微重力下植物对单价阳离子（P、K）超高吸收和二价阳离子（Ca、Mg、Fe、Mn等）吸收大幅下降的生理特征进行高阶补偿调配，极具科普趣味。

### 2. 📊 动态养分平衡雷达对照图 (Nutrient Balance Radar)
采用 **Plotly** 绘制动态极坐标雷达图，将用户当前配方与学术界黄金标尺 **Hoagland No. 2** 进行半透明重叠对照。
*   直观展示各肥料组分在营养液中的质量占比轮廓。
*   配有**“养分平衡轮廓深度解密”**模块，动态刷新科普说明，极大提升用户在网页端的停留时间。

### 3. 🧪 实时 pH 化学安全性预警与 lockout 拦截
根据水质背景进行动态化学稳定性判定：
*   **pH 超过 6.5 红色预警**：自动提示“铁沉淀及 lockout 锁死风险”，并科普如何引入 **EDDHA 螯合铁** 或调低 pH 予以解决。
*   **pH 低于 5.5 黄色预警**：提示强酸性环境下的根系损伤与钙镁吸收障碍。

### 4. 📝 傻瓜式 A/B 母液分罐混溶工艺 (5步标准防沉淀法)
根据水量单位（L/GAL）及目标 EC 浓度自动折算：
*   **A 罐**：富集钙源、硝态氮源。
*   **B 罐**：富集硫酸盐、磷酸盐及微量元素。
*   提供标准的“温水溶解 $\rightarrow$ A 稀释 $\rightarrow$ B 混匀”五步实操指南，严防硫酸钙与磷酸铁等不溶性化学沉淀。

---

## 🛠️ 本地极速运行 (Local Setup)

本应用采用 **Streamlit** 极简网页框架进行开发。您无需掌握繁琐的前端、后端及服务器配置，即可在本地电脑一键运行：

### 1. 克隆/下载本仓库到本地
```bash
git clone https://github.com/您的用户名/hydroponic-calculator.git
cd hydroponic-calculator
```

### 2. 安装依赖包
我们已将运行所需的第三方库封装在 `requirements.txt` 中。请确保您的 Python 环境在 3.9 及以上：
```bash
pip install -r requirements.txt
```

### 3. 启动本地 Streamlit 网页
```bash
streamlit run app.py
```
运行后，浏览器将自动弹出本地服务器地址：`http://localhost:8501`。

---

## 🚀 云端部署 (Streamlit Community Cloud)

您可以极其轻松地将本项目部署到云端服务器，免费生成一个全球可访问的专属网站链接：

1. 登录 [Streamlit Share](https://share.streamlit.io/) 并绑定您的 GitHub 账号。
2. 点击 **New app**。
3. 选择您克隆好的 GitHub 仓库，主分支选择 `main`，主程序路径选择 `app.py`。
4. 点击 **Deploy**，等待约 1 分钟即可完成部署！

---

## 🛒 商业变现设计 (Monetization Layout)

本程序在计算结果面板下方预留了精美的**联盟营销（Affiliate Marketing）广告和推荐购买卡片**。您可以直接在 `app.py` 源码中将以下推广链接修改为您的返利链接（如亚马逊联盟、淘宝客或独立站）：
*   **高精度电子天平 (0.01g)**：精准称量微量元素。
*   **避光 A/B 母液储水罐 (5L)**：延长母液活性，防藻防光解。
*   **高溶解度 EDDHA 螯合铁 (红粉)**：高 pH 硬水环境下攻克西红柿/生菜黄叶病的特效药。

---

## 📄 开源许可证 (License)

本项目采用 **MIT License**。您可以自由地复制、修改和商业化，发布在您自己的网站或博客中以赚取流量和广告收益。

---
🌿 *项目基于《水培耕作：现代技术与实践指南》科学理论开发，致力于让植物水培更严谨、更简单、更高产。*
