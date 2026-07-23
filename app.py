#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
プログラム名称: データ登録・確認アプリ
作成日: 2026-07-08
説明: Streamlitを使用したデータ管理システム。
      データの登録、一覧表示、統計解析機能を提供します。
"""

# ==========================================
# 1. ライブラリのインポート
# ==========================================
# 標準ライブラリ
import json
import os
from datetime import datetime

# 外部ライブラリ
import pandas as pd
import streamlit as st
import plotly.express as px

# ==========================================
# 2. 定数・設定の定義
# ==========================================
DATA_FILE = 'data.json'

# ==========================================
# 3. データの入出力関数 (Utility functions)
# ==========================================
def init_data_file():
    """データファイルが存在しない場合は初期化する"""
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=2)

def load_data():
    """ファイルを読み込んでデータを返す"""
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_data(data):
    """データをファイルに保存する"""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ==========================================
# 4. 各ページの表示処理 (UI functions)
# ==========================================
# 指示: 処理の見通しを良くするため、ページごとに処理を関数化することを推奨します

def show_registration_page():
    """データ登録ページの表示"""


    if st.session_state.get("clear_form", False):

    
        st.session_state.amount = 0
        st.session_state.cost = 0
        st.session_state.quantity = 0

        st.session_state.contract_no = ""
        st.session_state.product_name = ""
        st.session_state.address = ""
        
        st.session_state.clear_form = False

    if "amount" not in st.session_state:
        st.session_state.amount = 0

    if "cost" not in st.session_state:
        st.session_state.cost = 0

    if "quantity" not in st.session_state:
        st.session_state.quantity = 0
    
    if "contract_no" not in st.session_state:
        st.session_state.contract_no = ""

    if "product_name" not in st.session_state:
        st.session_state.product_name = ""

    if "address" not in st.session_state:
        st.session_state.address = ""

            

    

    if st.session_state.get("show_success", False):
        st.success("✅ データが登録されました！")
        st.balloons()
        st.session_state["show_success"] = False



    st.caption("※ 🔴：必須項目")


    col1, col2 = st.columns(2)

    with col1:

        date = st.date_input("🔴日付")

        person_in_charge = st.text_input( "🔴担当者", placeholder="例: 田中太郎" )

        contract_no = st.text_input( "契約NO", placeholder="例: CT-001", key="contract_no" )

        product_name = st.text_input( "🔴商品名", placeholder="例: 商品A", key="product_name" )

        address = st.text_input( "住所", placeholder="例: 東京都渋谷区", key="address" )


    with col2:

        amount = st.number_input( "🔴単価（円）", min_value=0, key="amount" )
        
        cost = st.number_input( "🔴原価（円）", min_value=0, key="cost" )

        quantity = st.number_input( "🔴数量", min_value=0, key="quantity" )


        # 自動計算
        calc_total_amount = amount * quantity
        calc_total_cost = cost * quantity

    
        metric_left, metric_right = st.columns([1, 2])

        with metric_right:
            st.metric( "合計金額（円）", f"{calc_total_amount:,.0f}" )
            st.metric( "合計原価（円）", f"{calc_total_cost:,.0f}" )


        
    
    #登録ボタン
    submit_button = st.button( "✅ 登録する", use_container_width=True )


        
    if submit_button:
            
        # 単価・原価の下2桁を切り捨て

            amount_trunc = (
                int(amount)
                if int(amount) < 100
                else (int(amount) // 100) * 100
            )

            cost_trunc = (
                int(cost)
                if int(cost) < 100
                else (int(cost) // 100) * 100
            )

            total_amount_trunc = (
                int(calc_total_amount)
                if int(calc_total_amount) < 100
                else (int(calc_total_amount) // 100) * 100
            )

            total_cost_trunc = (
                int(calc_total_cost)
                if int(calc_total_cost) < 100
                else (int(calc_total_cost) // 100) * 100
            )

            
            if not all([ date, person_in_charge, quantity, amount, product_name, cost ]):

                st.error("❌ すべての必須項目を入力してください")


            elif (
                total_amount_trunc is not None
                and total_cost_trunc is not None
                and total_amount_trunc > 0
                and total_cost_trunc > total_amount_trunc / 2
            ):
                st.error(
                    f"❌ 合計原価は合計金額の1/2以下で入力してください。"
                    f"（現在の上限: {int(total_amount_trunc / 2):,}円）"
                )



            else:

                new_entry = {
                    'id': datetime.now().strftime('%Y%m%d%H%M%S'),
                    'date': str(date),
                    'amount': str(amount_trunc),
                    'contract_no': contract_no,
                    'quantity': str(int(quantity)),
                    'person_in_charge': person_in_charge,
                    'product_name': product_name,
                    'address': address,
                    'cost': str(cost_trunc),
                    'total_amount': str(total_amount_trunc),
                    'total_cost': str(total_cost_trunc),
                    'registered_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }

                
                data = load_data()
                data.append(new_entry)
                
                save_data(data)

                st.session_state["clear_form"] = True
                st.session_state["show_success"] = True

                st.rerun()




def show_list_page():
    """データ一覧ページの表示"""

    st.header("登録済みデータ一覧")
    data = load_data()
    if not data:
        st.info("📌 登録されたデータがありません")
    else:
        df = pd.DataFrame(data)
        # =====================================
        # 検索条件
        # =====================================
   
        search_clicked = st.button(
            "🔍 検索",
            use_container_width=True
        )


        if "search_clicked" not in st.session_state:
            st.session_state.search_clicked = False
   


        st.subheader("🔍 検索フィルタ")

        filter_col1, filter_col2 = st.columns(2)

        with filter_col1:

            filter_date = st.text_input(
                "日付",
                placeholder="例: 2026-07-09"
            )

            filter_person = st.text_input(
                "担当者",
                placeholder="例: 田中"
            )

            filter_contract = st.text_input(
                "契約NO",
                placeholder="例: CT-001"
            )

        with filter_col2:

            filter_product = st.text_input(
                "商品名",
                placeholder="例: 商品A"
            )

            filter_address = st.text_input(
                "住所",
                placeholder="例: 福岡"
            )

        # =====================================
        # フィルタ処理
        # =====================================

        if search_clicked:

            if filter_date:
                df = df[
                    df["date"].astype(str).str.contains(
                        filter_date,
                        case=False,
                        na=False
                    )
                ]

            if filter_person:
                df = df[
                    df["person_in_charge"].astype(str).str.contains(
                        filter_person,
                        case=False,
                        na=False
                    )
                ]

            if filter_contract:
                df = df[
                    df["contract_no"].astype(str).str.contains(
                        filter_contract,
                        case=False,
                        na=False
                    )
                ]

            if filter_product:
                df = df[
                    df["product_name"].astype(str).str.contains(
                        filter_product,
                        case=False,
                        na=False
                    )
                ]

            if filter_address:
                df = df[
                    df["address"].astype(str).str.contains(
                        filter_address,
                        case=False,
                        na=False
                    )
                ]





        st.caption(
            f"検索結果: {len(df)} 件"
        )


        df['amount'] = df['amount'].astype(int).apply(lambda x: f"{x:,}円")
        df['cost'] = df['cost'].astype(int).apply(lambda x: f"{x:,}円")
        df['total_amount'] = (
            df['total_amount']
            .astype(int)
            .apply(lambda x: f"{x:,}円")
        )

        df['total_cost'] = (
            df['total_cost']
            .astype(int)
            .apply(lambda x: f"{x:,}円")
        )
                
        display_columns = [
            'date',
            'person_in_charge',
            'contract_no',
            'product_name',
            'address',
            'amount',
            'cost',
            'total_amount',
            'total_cost',
            'quantity',
            'registered_at'
        ]
        
        df_display = df[display_columns].copy()
        

        df_display.columns = [
            '日付',
            '担当者',
            '契約NO',
            '商品名',
            '住所',
            '単価',
            '原価',
            '合計金額',
            '合計原価',
            '数量',
            '登録日時'
        ]

        df_display.insert(0, "削除", False)


        
        edited_df = st.data_editor( df_display, use_container_width=True, hide_index=True)

        # 一覧の直下に削除成功メッセージ表示
        if st.session_state.get("delete_success", False):

            st.success(
                f"✅ {st.session_state.delete_count}件のデータを削除しました！"
            )

            st.session_state.delete_success = False

                # 削除確認フラグ
        if "show_delete_confirm" not in st.session_state:
            st.session_state.show_delete_confirm = False

        if "delete_rows" not in st.session_state:
            st.session_state.delete_rows = []
        

    # 削除ボタン
    if st.button(
        "🗑️ 選択したデータを削除",
        use_container_width=True
    ):

        delete_rows = edited_df[
            edited_df["削除"] == True
        ].index.tolist()

        if delete_rows:
            st.session_state.delete_rows = delete_rows
            st.session_state.show_delete_confirm = True
        else:
            st.warning(
                "削除するデータを選択してください"
            )

    # 確認メッセージ
    if st.session_state.show_delete_confirm:

        st.warning(
            f"選択した {len(st.session_state.delete_rows)} 件のデータを削除しますか？"
        )

        col_yes, col_no = st.columns(2)

        with col_yes:
            if st.button(
                "✅ はい、削除します",
                use_container_width=True
            ):

                new_data = [
                    item
                    for idx, item in enumerate(data)
                    if idx not in st.session_state.delete_rows
                ]

                
                save_data(new_data)

                st.session_state.delete_count = len(
                    st.session_state.delete_rows
                )

                st.session_state.delete_success = True

                st.session_state.show_delete_confirm = False
                st.session_state.delete_rows = []

                st.rerun()


        with col_no:
            if st.button(
                "❌ キャンセル",
                use_container_width=True
            ):
                st.session_state.show_delete_confirm = False
                st.rerun()


    
    # CSVダウンロード
    st.divider()
    
    csv = df_display.to_csv( index=False ).encode("utf-8-sig")

    
    st.download_button(
        label="📥 CSVでダウンロード",
        data=csv,
        file_name=f"data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
        mime="text/csv",
        use_container_width=True
    )



def show_stats_page():
    """統計情報の表示"""
    st.header("📈 統計情報")
    data = load_data()
    if not data:
        st.info("📌 登録されたデータがありません")
    else:

        df_stats = pd.DataFrame(data)

        df_stats['amount'] = df_stats['amount'].astype(int)
        df_stats['cost'] = df_stats['cost'].astype(int)

        df_stats['total_amount'] = df_stats['total_amount'].astype(int)
        df_stats['total_cost'] = df_stats['total_cost'].astype(int)



        # フィルタ後に集計
        total_records = len(df_stats)
        total_amount = df_stats["total_amount"].sum()
        total_cost = df_stats["total_cost"].sum()
        total_quantity = df_stats["quantity"].astype(int).sum()

           
        profit = total_amount - total_cost
        profit_rate = (profit / total_amount * 100) if total_amount > 0 else 0

        # メトリクス表示
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("登録件数", f"{total_records}件")
        with col2:
            st.metric("総売上", f"¥{total_amount:,.0f}")
        with col3:
            st.metric("総原価", f"¥{total_cost:,.0f}")
        with col4:
            st.metric("利益", f"¥{profit:,.0f}", f"{profit_rate:.1f}%")

        st.divider()


        df_stats['profit'] = (
            df_stats['total_amount']
            - df_stats['total_cost']
        )

        st.subheader("📊 売上推移")


        df_amount_by_date = (
            df_stats.groupby('date')['total_amount']
            .sum()
            .reset_index()
        )

        st.line_chart(
            df_amount_by_date.set_index('date')
        )

        st.divider()

        # =====================================
        # 月別 商品別売上構成（円グラフ）
        # =====================================
        st.subheader("🥧 月別 商品別売上構成")

        df_stats['year_month'] = (
            df_stats['date'].astype(str).str[:7]
        )

        month_list = sorted(
            [
                m
                for m in df_stats['year_month'].dropna().unique()
                if str(m).strip() != ""
            ],
            reverse=True
        )

        if month_list:

            selected_month = st.selectbox(
                "📅 月を選択してください",
                options=month_list
            )

            df_month = df_stats[
                df_stats['year_month'] == selected_month
            ]

            df_month_by_product = (
                df_month.groupby('product_name')['total_amount']
                .sum()
                .reset_index()
            )

            # 商品名未入力を除外
            df_month_by_product = df_month_by_product[
                df_month_by_product['product_name']
                .astype(str).str.strip() != ""
            ]

            # 商品別原価集計
            df_month_cost_by_product = (
                df_month.groupby('product_name')['total_cost']
                .sum()
                .reset_index()
            )

            # 商品名未入力を除外
            df_month_cost_by_product = df_month_cost_by_product[
                df_month_cost_by_product['product_name']
                .astype(str).str.strip() != ""
            ]



            # 2列レイアウト
            col_cost, col_sales = st.columns(2)

            # ==========================
            # 左側：原価
            # ==========================
            with col_cost:

                st.markdown("### 💰 商品別原価構成")

                if not df_month_cost_by_product.empty:

                    fig_cost_pie = px.pie(
                        df_month_cost_by_product,
                        values="total_cost",
                        names="product_name",
                        title=f"{selected_month} の商品別原価割合"
                    )

                    st.plotly_chart(
                        fig_cost_pie,
                        use_container_width=True
                    )

                else:
                    st.info(
                        f"📌 {selected_month} は商品別原価データがありません"
                    )

            # ==========================
            # 右側：売上
            # ==========================
            with col_sales:

                st.markdown("### 📈 商品別売上構成")

                if not df_month_by_product.empty:

                    fig_pie = px.pie(
                        df_month_by_product,
                        values="total_amount",
                        names="product_name",
                        title=f"{selected_month} の商品別売上割合"
                    )

                    st.plotly_chart(
                        fig_pie,
                        use_container_width=True
                    )

                else:
                    st.info(
                        f"📌 {selected_month} は商品別売上データがありません"
                    )




        else:
            st.info("📌 表示できる月のデータがありません")


        st.subheader("🏆 商品別売上")

        # =====================================
        # 商品フィルタ
        # =====================================

        product_list = sorted(
            [
                p
                for p in df_stats["product_name"].dropna().unique()
                if str(p).strip() != ""
            ]
        )

        selected_products = st.multiselect(
            "🔍 商品名で絞り込み",
            options=product_list,
            placeholder="商品名を検索して選択してください"
        )

        if selected_products:
            df_stats = df_stats[
                df_stats["product_name"].isin(selected_products)
            ]

        if df_stats.empty:
            st.warning("該当する商品データがありません")
            return
        

        df_by_product = (
            df_stats.groupby('product_name')['total_amount']
            .sum()
            .sort_values(ascending=False)
        )

        # 商品名未入力を除外
        df_by_product = df_by_product[
            df_by_product.index.astype(str).str.strip() != ""
        ]

        if not df_by_product.empty:
            st.bar_chart(df_by_product)
        else:
            st.info("商品別売上データがありません")



        st.subheader("💰 利益分析")

        col1, col2 = st.columns(2)

        with col1:

            df_profit_by_product = (
                df_stats.groupby('product_name')
                .apply(
                    lambda x:
                    (
                        x['profit'].sum()
                        / x['total_amount'].sum()
                        * 100
                    )
                    if x['total_amount'].sum() > 0
                    else 0
                )
                .sort_values(ascending=False)
            )

            # 商品名未入力を除外
            df_profit_by_product = df_profit_by_product[
                df_profit_by_product.index.astype(str).str.strip() != ""
            ]

            st.write("**商品別利益率チャート**")

            if not df_profit_by_product.empty:
                st.bar_chart(df_profit_by_product)
            else:
                st.info("利益率データがありません")

        with col2:

            st.write("**商品別利益率（%）**")

            for product, rate in df_profit_by_product.items():
                st.write(
                    f"{product}: {rate:.1f}%"
                )

# ==========================================
# 5. メイン実行処理
# ==========================================
def main():
    """アプリのメインロジック"""
    
    # ページ設定 (指示: メイン処理の最初に一度だけ呼び出すのが一般的です)
    st.set_page_config(
        page_title="📊 データ登録・確認アプリ",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # 初期化処理
    init_data_file()

    # ヘッダー表示
    st.title("📊 データ登録・確認アプリ")
    st.markdown("シンプルで使いやすいデータ登録・管理アプリケーション")

    # サイドバーメニュー
    with st.sidebar:
        st.header("📋 メニュー")
        page = st.radio("選択してください", ["データ登録", "データ一覧", "統計情報"])

    # ページ切り替え
    if page == "データ登録":
        show_registration_page()
    elif page == "データ一覧":
        show_list_page()
    elif page == "統計情報":
        show_stats_page()

    # フッター
    st.divider()
    st.caption("© 2024 データ登録・確認アプリ | Streamlit版")

# プログラムの実行起点
if __name__ == "__main__":
    main()