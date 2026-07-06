import streamlit as st
import pandas as pd
from rules.alteration_rules import (
    identify_minerals,
    calculate_matches,
    interpret_alteration,
    get_evidence,
    confidence_level,
    generate_interpretation
)
import matplotlib.pyplot as plt
from pathlib import Path

# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="ALTERA",
    page_icon="🪨",
    layout="wide"
)

# ==================================================
# CUSTOM CSS
# ==================================================

st.markdown("""
<style>

.block-container{
    padding-top:2rem;
    padding-bottom:2rem;
}

h1{
    color:#1f4e79;
}

h2{
    color:#2f6690;
}

div.stButton > button{
    width:100%;
    border-radius:12px;
    height:50px;
    font-weight:bold;
}

div[data-testid="stMetric"]{
    border:1px solid #dddddd;
    padding:15px;
    border-radius:12px;
}

</style>
""",unsafe_allow_html=True)

# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.title("🪨 ALTERA")

st.sidebar.write("""
Hydrothermal Alteration Interpretation Platform
""")

st.sidebar.write("---")

st.sidebar.subheader("⚙️ Analysis Settings")

mineral_threshold = st.sidebar.slider(
    "Minimum Mineral Content (%)",
    min_value=0.0,
    max_value=20.0,
    value=5.0,
    step=0.5,
    help="Minerals with abundance below this value will be ignored during interpretation."
)

st.sidebar.divider()

menu = st.sidebar.radio(

"Navigation",

[
"🏠 Home",
"📂 Data Processing",
"📥 Templates",
"📄 About"
]

)

st.sidebar.divider()

st.sidebar.info("Version 2.0")

# ==================================================
# HOME
# ==================================================

if menu=="🏠 Home":

    st.title("🪨 ALTERA")

    st.subheader(
        "Hydrothermal Alteration Interpretation Platform"
    )

    st.write("---")

    st.markdown("""
### Transforming XRD & XRF into Hydrothermal Insights

ALTERA merupakan platform berbasis web
yang membantu interpretasi awal alterasi
hidrotermal menggunakan data XRD dan XRF.

Platform ini dikembangkan agar mahasiswa,
peneliti, maupun praktisi eksplorasi dapat
melakukan visualisasi, pengolahan data,
serta interpretasi awal secara otomatis.
""")

    st.write("")

    c1,c2,c3,c4=st.columns(4)

    with c1:

        st.success("""
📂

Upload

Dataset
""")

    with c2:

        st.success("""
📊

Automatic

Processing
""")

    with c3:

        st.success("""
📈

Geochemical

Plot
""")

    with c4:

        st.success("""
🔥

Alteration

Interpretation
""")

    st.write("")

    st.info("""
Supported File Format

✅ Excel (.xlsx)

✅ CSV (.csv)
""")
    # ==================================================
# DATA PROCESSING
# ==================================================

elif menu=="📂 Data Processing":

    st.title("📂 Data Processing")

    st.caption(
        "Upload XRF and XRD datasets before performing hydrothermal alteration interpretation."
    )

    st.write("---")

    # ==========================
    # REQUIRED COLUMNS
    # ==========================

    required_xrf = [
        "Sample",
        "SiO2",
        "TiO2",
        "Al2O3",
        "Fe2O3",
        "MgO",
        "CaO",
        "Na2O",
        "K2O",
        "MnO",
        "P2O5",
        "LOI"
    ]

    required_xrd = [
        "Sample",
        "Quartz",
        "Plagioclase",
        "K-Feldspar",
        "Albite",
        "Sericite",
        "Illite",
        "Muscovite",
        "Biotite",
        "Kaolinite",
        "Smectite",
        "Dickite",
        "Pyrophyllite",
        "Chlorite",
        "Epidote",
        "Actinolite",
        "Calcite",
        "Dolomite",
        "Ankerite",
        "Pyrite",
        "Magnetite",
        "Hematite",
        "Rutile",
        "Alunite",
        "Diaspore",
        "Zunyite"
    ]

    # ==========================
    # UPLOAD
    # ==========================

    col1,col2 = st.columns(2)

    with col1:

        st.subheader("🧪 XRF Dataset")

        xrf = st.file_uploader(

            "Upload XRF File",

            type=["csv","xlsx"],

            key="xrf"

        )

    with col2:

        st.subheader("🪨 XRD Dataset")

        xrd = st.file_uploader(

            "Upload XRD File",

            type=["csv","xlsx"],

            key="xrd"

        )

    st.write("---")

    # ==========================
    # READ DATA
    # ==========================

    data_xrf = None
    data_xrd = None

    if xrf is not None:

        if xrf.name.endswith(".csv"):

            data_xrf = pd.read_csv(xrf)

        else:

            data_xrf = pd.read_excel(xrf)

    if xrd is not None:

        if xrd.name.endswith(".csv"):

            data_xrd = pd.read_csv(xrd)

        else:

            data_xrd = pd.read_excel(xrd)

    # ==========================
    # PREVIEW
    # ==========================

    col1,col2 = st.columns(2)

    with col1:

        st.subheader("📋 XRF Preview")

        if data_xrf is not None:

            st.dataframe(
                data_xrf,
                use_container_width=True
            )

            missing=[]

            for col in required_xrf:

                if col not in data_xrf.columns:

                    missing.append(col)

            if len(missing)==0:

                st.success("✅ XRF template is valid.")

            else:

                st.error("Missing columns")

                st.write(missing)

        else:

            st.info("No XRF dataset uploaded.")

    with col2:

        st.subheader("📋 XRD Preview")

        if data_xrd is not None:

            st.dataframe(
                data_xrd,
                use_container_width=True
            )

            missing=[]

            for col in required_xrd:

                if col not in data_xrd.columns:

                    missing.append(col)

            if len(missing)==0:

                st.success("✅ XRD template is valid.")

            else:

                st.error("Missing columns")

                st.write(missing)

        else:

            st.info("No XRD dataset uploaded.")

    st.write("---")

    # ==========================
    # ANALYSIS
    # ==========================

    st.header("🧪 Analysis")

    ready = False

    if data_xrf is not None and data_xrd is not None:

        ready = True

    if ready:

        st.success("Datasets are ready for analysis.")

        if st.button("🚀 Generate Analysis"):

            st.subheader("📊 Geochemical Indices")
            
            result = data_xrf.copy()

            result["AI"] = (
                (
                    result["K2O"] +
                    result["MgO"]
                ) /
                (
                    result["K2O"] +
                    result["MgO"] +
                    result["Na2O"] +
                    result["CaO"]
                )
            ) * 100

        #=========================
        # CCPI
        #=========================

            result["CCPI"] = (
                (
                    result["MgO"] +
                    result["Fe2O3"]
                ) /
                (
                    result["MgO"] +
                    result["Fe2O3"] +
                    result["Na2O"] +
                    result["K2O"]
                )
            ) * 100

        #=========================
        # K/Na Ratio
        #=========================

            result["K/Na"] = result["K2O"] / result["Na2O"]

        #=========================
        # Mg Number
        #=========================

            result["Mg Number"] = (
                result["MgO"] /
                (
                    result["MgO"] +
                    result["Fe2O3"]
                )
            ) * 100

            st.dataframe(
                result[
                    [
                        "Sample", 
                        "AI",
                        "CCPI",
                        "K/Na",
                        "Mg Number"
                    ]
                ],
                use_container_width=True
            )

            st.subheader("📈 AI vs CCPI Plot")
            fig, ax = plt.subplots(figsize=(9,8))
            ax.scatter(
                result["AI"],
                result["CCPI"],
                s=120,
                color="red",
                edgecolor="black",
                linewidth=1
            )

            ax.set_xlim(0,100)
            ax.set_ylim(0,100)

            ax.grid(
                linestyle="--",
                alpha=0.4
            )

            ax.plot(
                [0,100],
                [100,0],
                color="black",
                linestyle="--",
                linewidth=2
            )

            ax.text(
                63,
                60,
                "Hydrothermal",
                rotation=-45,
                fontsize=12,
                color="black"
            )

            ax.text(
                18,
                25,
                "Diagenetic",
                rotation=-45,
                fontsize=12,
                color="black"
            )

            for i in range(len(result)):

                ax.text(
                    result["AI"].iloc[i],
                    result["CCPI"].iloc[i],
                    result["Sample"].iloc[i],
                    fontsize=8
                )

            ax.set_xlabel("Alteration Index (AI)")
            ax.set_ylabel("CCPI")
            ax.set_title("AI vs CCPI")
            ax.grid(True)

            st.pyplot(fig)

            st.write("---")

            st.header("🪨 Alteration Interpretation")

            summary = []

            for i in range(len(data_xrd)):

                sample = data_xrd.iloc[i]

                minerals = identify_minerals(
                    sample,
                    mineral_threshold
                )

                st.subheader(sample["Sample"])

                st.write("Detected Minerals:")

                for mineral in minerals:

                    st.markdown(f"✅ {mineral}")

                matches = calculate_matches(minerals)

                zone, score = interpret_alteration(matches)

                evidence = get_evidence(
                    minerals,
                    zone
                )

                confidence = confidence_level(score)

                summary.append({

                    "Sample": sample["Sample"],

                    "AI": round(result.loc[i, "AI"], 2),

                    "CCPI": round(result.loc[i, "CCPI"], 2),

                    "Zone": zone,

                    "Evidence": confidence

                })

                st.write("### Predicted Zone")
                st.success(zone)
                st.write("### Interpretation")
                interpretation = (
                    f"Sampel **{sample['Sample']}** diinterpretasikan sebagai "
                    f"**zona {zone}** karena himpunan mineral yang teridentifikasi "
                    f"paling sesuai dengan karakteristik zona tersebut berdasarkan "
                    f"database ALTERA yang mengacu pada Corbett & Leach (1996)."
                )

                st.write(interpretation)
                if len(evidence["diagnostic"]) > 0:

                    diag = ", ".join(evidence["diagnostic"])

                    st.write(
                        f"Mineral diagnostik yang ditemukan yaitu **{diag}**."
                    )

                if len(evidence["common"]) > 0:

                    common = ", ".join(evidence["common"])

                    st.write(
                        f"Mineral umum yang mendukung interpretasi yaitu **{common}**."
                    )

                st.write(
                    "Interpretasi ini merupakan interpretasi awal berdasarkan "
                    "hasil identifikasi mineral XRD dan sebaiknya digunakan "
                    "bersama informasi geologi lapangan maupun data geokimia."
                )

                st.write("### Evidence")

                # Diagnostic
                st.markdown("**Diagnostic Minerals**")

                if len(evidence["diagnostic"]) > 0:

                    for mineral in evidence["diagnostic"]:

                        st.markdown(f"🟢 {mineral}")

                else:

                    st.write("-")

                # Common

                st.markdown("**Common Minerals**")

                if len(evidence["common"]) > 0:

                    for mineral in evidence["common"]:

                        st.markdown(f"🔵 {mineral}")

                else:

                    st.write("-")

                # Possible

                st.markdown("**Possible Minerals**")

                if len(evidence["possible"]) > 0:

                    for mineral in evidence["possible"]:

                        st.markdown(f"🟡 {mineral}")

                else:

                    st.write("-")

                st.write("### Confidence")
                st.info(confidence)

                st.write("---")

                st.subheader("📋 Interpretation Summary")

                summary_df = pd.DataFrame(summary)

                st.dataframe(
                    summary_df,
                    use_container_width=True
                )

    else:

        st.warning(
            "Please upload both XRF and XRD datasets."
        )

# ==================================================
# TEMPLATES
# ==================================================

elif menu=="📥 Templates":

    st.title("📥 ALTERA Templates")

    st.write(
        """
Download template resmi ALTERA sebelum melakukan upload data.
"""
    )

    st.write("---")

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("🧪 XRF Template")

        st.write("""
Gunakan template ini untuk data geokimia hasil analisis XRF.
""")

        template_xrf = Path("templates/templates_xrf_template.xlsx")

        if template_xrf.exists():

            with open(template_xrf, "rb") as file:

                st.download_button(

                    "📥 Download XRF Template",

                    file,

                    file_name="ALTERA_XRF_Template.xlsx"

                )

        else:

            st.warning("Template XRF belum tersedia.")

    with col2:

        st.subheader("🪨 XRD Template")

        st.write("""
Gunakan template ini untuk data mineralogi hasil analisis XRD.
""")

        template_xrd = Path("templates/templates_xrd_template.xlsx")

        if template_xrd.exists():

            with open(template_xrd, "rb") as file:

                st.download_button(

                    "📥 Download XRD Template",

                    file,

                    file_name="ALTERA_XRD_Template.xlsx"

                )

        else:

            st.warning("Template XRD belum tersedia.")

    st.write("---")

    st.success("Gunakan template resmi ALTERA agar format data sesuai.")

# ==================================================
# ABOUT
# ==================================================

elif menu=="📄 About":

    st.title("📄 About ALTERA")

    st.write("---")

    st.subheader("🪨 What is ALTERA?")

    st.write("""
ALTERA (Alteration Analysis Platform) merupakan platform berbasis web yang dikembangkan untuk membantu interpretasi awal alterasi hidrotermal menggunakan data XRD dan XRF.

Platform ini dirancang untuk mengintegrasikan proses upload data, validasi, visualisasi, dan interpretasi awal alterasi hidrotermal dalam satu sistem yang sederhana dan mudah digunakan.
""")

    st.write("---")

    st.subheader("🎯 Main Features")

    st.markdown("""

- 📂 Upload data XRF

- 🪨 Upload data XRD

- 📋 Validasi template otomatis

- 📈 Visualisasi data geokimia

- 🔥 Interpretasi awal zona alterasi

- 📄 Pengembangan laporan otomatis

""")

    st.write("---")

    st.subheader("👥 Target Users")

    st.markdown("""

- Mahasiswa Geologi

- Peneliti

- Praktisi Eksplorasi Mineral

- Akademisi

""")

    st.write("---")

    st.subheader("🚀 Version")

    st.info("ALTERA Version 2.0")

    st.caption(
        "Developed for Hydrothermal Alteration Interpretation."
    )