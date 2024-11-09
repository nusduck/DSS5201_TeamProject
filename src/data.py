import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px


# 读取数据
data = pd.read_excel("../data/Social_Media_Usage_pivoted.xlsx")
data2 = pd.read_csv(
    "../data/which_social_media_platforms_are_most_popular_data_2024-01-31.csv",
    skiprows=2,
    skipfooter=3,
    engine='python'  # 添加 engine 参数以避免警告
)

# 数据清洗
data2.columns = data2.columns.str.replace('\t', '')
data2 = data2.replace('\t', '', regex=True)

# 改变数据类型
data2['Year'] = pd.to_datetime(data2['Year'])
for i in data2.columns[1:]:
    data2[i] = data2[i].str.replace('%', '').astype(float) / 100

# 获取年份列表
x_l = data2['Year'].dt.to_period('Y').dt.start_time.unique()
x_ll = data2['Year'].dt.to_period('Y').dt.start_time.unique().strftime('%Y')

def main():
    # 标题居中

    st.markdown("<h1 style='text-align: center;'>Assignment</h1>", unsafe_allow_html=True)

    # 使用所有平台
    selected_platforms = list(data2.columns[1:])  # 所有平台

    # 筛选数据
    df = data2[['Year'] + selected_platforms]

    # 将数据从宽表转换为长表
    df_melted = df.melt(id_vars='Year', value_vars=selected_platforms, var_name='Platform', value_name='Usage')

    # 创建 Plotly 图表，使用 x_ll 作为 x 轴标签
    fig = px.line(
        df_melted,
        x='Year',
        y='Usage',
        color='Platform',
        markers=True,
        labels={
            'Year': 'Year',
            'Usage': 'Usage',
            'Platform': 'Platform'
        },
        title='Which social media platforms are most popular'
    )

    # 更新布局
    fig.update_layout(
        width=800,
        font=dict(family='Times New Roman', size=16),
        title=dict(
            text='Which social media platforms are most popular<br><i>% of U.S. adults who say they ever use...</i>',
            x=.05,
            y=0.95,
            xanchor='left',
            yanchor='top',
            font=dict(size=16, family='Times New Roman')
        ),
        xaxis=dict(
            tickformat='%Y',
            # dtick='M12',  # 每年一个刻度
            tickvals=x_ll,
            ticktext=x_ll,
            tickfont=dict(family='Times New Roman')
        ),
        yaxis=dict(
            tickformat='.0%',
            range=[0, 1],
            tickfont=dict(family='Times New Roman')
        ),
        legend=dict(
            title='Platform',
            font=dict(family='Times New Roman'),
            x=1.05,
            y=0.5,
            traceorder='normal'
        ),
        margin=dict(l=50, r=150, t=100, b=50)
    )
    # 添加垂直线
    fig.add_vline(
        x=pd.to_datetime('2022-01-01'),
        line=dict(color='grey', dash='solid')
    )

    # 添加注释
    fig.add_annotation(
        x=pd.to_datetime('2022-01-01'),
        y=0.9,
        text='Change in survey mode--',
        showarrow=False,
        font=dict(color='grey', size=12),
        xanchor='right',
        yanchor='bottom'
    )

    fig.update_traces(connectgaps=True)

    # 在 Streamlit 中显示图表，使用容器的全部宽度
    st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    main()