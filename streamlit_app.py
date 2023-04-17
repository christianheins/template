def main():
    import requests
    import pandas as pd
    import streamlit as st
    from streamlit_option_menu import option_menu
    from st_pages import Page, show_pages, add_page_title
    import numpy as np
    import altair as alt
    import urllib.parse
    import os
    import datetime as dt
    import base64
    from github import Github
    from github import InputFileContent

    pd.set_option('display.max_columns', None)

    #Streamlit
    st.set_page_config(page_title="WG Gesucht Analysis", layout="wide", initial_sidebar_state="expanded", menu_items={
        'Get Help': 'https://www.extremelycoolapp.com/help',
        'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# This is a header. This is an *extremely* cool app!"
    })

    #Pages
    page_real_estate_general_dashboard = "ambelin.py"
    page_maps = "pages/maps.py"

    show_pages(
        [
            Page(page_real_estate_general_dashboard, "General Dashboard", "🏠"),
            Page(page_maps, "Maps", "🗺️"),
        ]
    )

    with open('style.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    nameofdataframe = "df_concat.csv"

    with st.sidebar:
        st.sidebar.header("Sections")
        selected = option_menu(
            menu_title="Menu",
            options=["🏘️ Apartments", "🫂 Neighbourhoods", "📑 Sample contracts"], #https://icons.getbootstrap.com/
            orientation="vertical",
        )

        #Create a button
        button_pressed = False
        st.markdown("""---""")
        st.markdown("<p style='text-align: center; color: red;'>Click to refresh the WG-Gesucht dataframe</p>", unsafe_allow_html=True)
        if st.button("Refresh", use_container_width=True):
            button_pressed = True
            st.write("Button pressed!")

            def requestswg_all():

                df_toupdate = []
                for i in range(0,50):

                    url = f"https://www.wg-gesucht.de/1-zimmer-wohnungen-und-wohnungen-in-Berlin.8.1+2.0.{i}.html?pagination=1&pu="
                    headers = {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
                    }
                    response = requests.get(url, headers=headers)
                    print(response)

                    dfs = pd.read_html(response.content)
                    df = dfs[0]  # assuming the desired table is the first one on the page
                    #for df in dfs:
                    #    print(df)

                    # Format the dataframe
                    df['frei bis'] = pd.to_datetime(df['frei bis'], dayfirst=True)
                    df['frei ab'] = pd.to_datetime(df['frei ab'], dayfirst=True)
                    df["Größe"] = df['Größe'].str.replace("m²","")
                    df["Miete"] = df['Miete'].str.replace(" €","")
                    df["Miete"] = df['Miete'].str.replace("€","")
                    df[["Miete", "Größe"]] = df[["Miete", "Größe"]].astype(float)
                    df["Lease term"] = df["frei bis"] - df["frei ab"]
                    #print(df.columns)
                    #print(df["Lease term"])

                    # Create two date objects
                    date1 = pd.to_datetime('2022-03-20')
                    date2 = pd.to_datetime('2022-03-25')

                    # Calculate the difference between the two dates
                    diff = date2 - date1

                    # Print the difference in days

                    #print(diff.days)


                    df['Lease term'] = (df['frei bis'].dt.year - df['frei ab'].dt.year) * 12 + (df['frei bis'].dt.month - df['frei ab'].dt.month)

                    df["EUR / SQM"] = df["Miete"] / df["Größe"]
                    #print(df)
                    df_toupdate.append(df)

                df = pd.concat(df_toupdate)
                return df

            def requestswg():

                '''
                url = "https://www.wg-gesucht.de/1-zimmer-wohnungen-und-wohnungen-in-Berlin.8.1+2.0.0.html"

                # Add headers to mimic a browser request
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
                }

                response = requests.get(url, headers=headers)

                # check the status code of the response
                print(response.status_code)

                # access the content of the response
                html_content = response.content
                print(html_content)
                '''

                #url = "https://www.wg-gesucht.de/1-zimmer-wohnungen-und-wohnungen-in-Berlin.8.1+2.0.0.html"
                url = "https://www.wg-gesucht.de/1-zimmer-wohnungen-und-wohnungen-in-Berlin.8.1+2.0.0.html?offer_filter=1&city_id=8&sort_order=0&noDeact=1&categories%5B%5D=1&categories%5B%5D=2&rent_types%5B%5D=0#back_to_ad_9597345"
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
                }
                response = requests.get(url, headers=headers)
                print(response)

                dfs = pd.read_html(response.content)
                df = dfs[0]  # assuming the desired table is the first one on the page
                #for df in dfs:
                #    print(df)

                # Format the dataframe
                df['frei bis'] = pd.to_datetime(df['frei bis'], dayfirst=True)
                df['frei ab'] = pd.to_datetime(df['frei ab'], dayfirst=True)
                df["Größe"] = df['Größe'].str.replace("m²","")
                df["Miete"] = df['Miete'].str.replace(" €","")
                df["Miete"] = df['Miete'].str.replace("€","")
                df[["Miete", "Größe"]] = df[["Miete", "Größe"]].astype(float)
                df["Lease term"] = df["frei bis"] - df["frei ab"]
                #print(df.columns)
                #print(df["Lease term"])

                # Create two date objects
                date1 = pd.to_datetime('2022-03-20')
                date2 = pd.to_datetime('2022-03-25')

                # Calculate the difference between the two dates
                diff = date2 - date1

                # Print the difference in days

                #print(diff.days)


                df['Lease term'] = (df['frei bis'].dt.year - df['frei ab'].dt.year) * 12 + (df['frei bis'].dt.month - df['frei ab'].dt.month)

                df["EUR / SQM"] = df["Miete"] / df["Größe"]
                #print(df)
                return df

            def requestswg2():

                '''
                url = "https://www.wg-gesucht.de/1-zimmer-wohnungen-und-wohnungen-in-Berlin.8.1+2.0.0.html"

                # Add headers to mimic a browser request
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
                }

                response = requests.get(url, headers=headers)

                # check the status code of the response
                print(response.status_code)

                # access the content of the response
                html_content = response.content
                print(html_content)
                '''

                #url1 = "https://www.wg-gesucht.de/1-zimmer-wohnungen-und-wohnungen-in-Berlin.8.1+2.0.0.html"
                url2 = "https://www.wg-gesucht.de/1-zimmer-wohnungen-und-wohnungen-in-Berlin.8.1+2.0.1.html?pagination=1&pu="
                url3 = "https://www.wg-gesucht.de/1-zimmer-wohnungen-und-wohnungen-in-Berlin.8.1+2.0.2.html?pagination=1&pu="
                url4 = "https://www.wg-gesucht.de/1-zimmer-wohnungen-und-wohnungen-in-Berlin.8.1+2.0.3.html?pagination=1&pu="

                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
                }
                response = requests.get(url2, headers=headers)

                dfs = pd.read_html(response.content)
                df = dfs[0]  # assuming the desired table is the first one on the page

                # Format the dataframe
                df['frei bis'] = pd.to_datetime(df['frei bis'], dayfirst=True)
                df['frei ab'] = pd.to_datetime(df['frei ab'], dayfirst=True)
                df["Größe"] = df['Größe'].str.replace("m²","")
                df["Miete"] = df['Miete'].str.replace(" €","")
                df["Miete"] = df['Miete'].str.replace("€","")
                df[["Miete", "Größe"]] = df[["Miete", "Größe"]].astype(float)
                df["Lease term"] = df["frei bis"] - df["frei ab"]
                #print(df.columns)
                #print(df["Lease term"])

                # Create two date objects
                date1 = pd.to_datetime('2022-03-20')
                date2 = pd.to_datetime('2022-03-25')

                # Calculate the difference between the two dates
                diff = date2 - date1

                # Print the difference in days

                #print(diff.days)


                df['Lease term'] = (df['frei bis'].dt.year - df['frei ab'].dt.year) * 12 + (df['frei bis'].dt.month - df['frei ab'].dt.month)

                df["EUR / SQM"] = df["Miete"] / df["Größe"]
                #print(df)
                return df

            def requestswg3():

                '''
                url = "https://www.wg-gesucht.de/1-zimmer-wohnungen-und-wohnungen-in-Berlin.8.1+2.0.0.html"

                # Add headers to mimic a browser request
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
                }

                response = requests.get(url, headers=headers)

                # check the status code of the response
                print(response.status_code)

                # access the content of the response
                html_content = response.content
                print(html_content)
                '''

                #url1 = "https://www.wg-gesucht.de/1-zimmer-wohnungen-und-wohnungen-in-Berlin.8.1+2.0.0.html"
                url2 = "https://www.wg-gesucht.de/1-zimmer-wohnungen-und-wohnungen-in-Berlin.8.1+2.0.1.html?pagination=1&pu="
                url3 = "https://www.wg-gesucht.de/1-zimmer-wohnungen-und-wohnungen-in-Berlin.8.1+2.0.2.html?pagination=1&pu="
                url4 = "https://www.wg-gesucht.de/1-zimmer-wohnungen-und-wohnungen-in-Berlin.8.1+2.0.3.html?pagination=1&pu="

                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
                }
                response = requests.get(url3, headers=headers)

                dfs = pd.read_html(response.content)
                df = dfs[0]  # assuming the desired table is the first one on the page

                # Format the dataframe
                df['frei bis'] = pd.to_datetime(df['frei bis'], dayfirst=True)
                df['frei ab'] = pd.to_datetime(df['frei ab'], dayfirst=True)
                df["Größe"] = df['Größe'].str.replace("m²","")
                df["Miete"] = df['Miete'].str.replace(" €","")
                df["Miete"] = df['Miete'].str.replace("€","")
                df[["Miete", "Größe"]] = df[["Miete", "Größe"]].astype(float)
                df["Lease term"] = df["frei bis"] - df["frei ab"]
                #print(df.columns)
                #print(df["Lease term"])

                # Create two date objects
                date1 = pd.to_datetime('2022-03-20')
                date2 = pd.to_datetime('2022-03-25')

                # Calculate the difference between the two dates
                diff = date2 - date1

                # Print the difference in days

                #print(diff.days)


                df['Lease term'] = (df['frei bis'].dt.year - df['frei ab'].dt.year) * 12 + (df['frei bis'].dt.month - df['frei ab'].dt.month)

                df["EUR / SQM"] = df["Miete"] / df["Größe"]
                #print(df)
                return df

            def requestswg4():

                '''
                url = "https://www.wg-gesucht.de/1-zimmer-wohnungen-und-wohnungen-in-Berlin.8.1+2.0.0.html"

                # Add headers to mimic a browser request
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
                }

                response = requests.get(url, headers=headers)

                # check the status code of the response
                print(response.status_code)

                # access the content of the response
                html_content = response.content
                print(html_content)
                '''

                #url1 = "https://www.wg-gesucht.de/1-zimmer-wohnungen-und-wohnungen-in-Berlin.8.1+2.0.0.html"
                url2 = "https://www.wg-gesucht.de/1-zimmer-wohnungen-und-wohnungen-in-Berlin.8.1+2.0.1.html?pagination=1&pu="
                url3 = "https://www.wg-gesucht.de/1-zimmer-wohnungen-und-wohnungen-in-Berlin.8.1+2.0.2.html?pagination=1&pu="
                url4 = "https://www.wg-gesucht.de/1-zimmer-wohnungen-und-wohnungen-in-Berlin.8.1+2.0.3.html?pagination=1&pu="

                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
                }
                response = requests.get(url4, headers=headers)

                dfs = pd.read_html(response.content)
                df = dfs[0]  # assuming the desired table is the first one on the page

                # Format the dataframe
                df['frei bis'] = pd.to_datetime(df['frei bis'], dayfirst=True)
                df['frei ab'] = pd.to_datetime(df['frei ab'], dayfirst=True)
                df["Größe"] = df['Größe'].str.replace("m²","")
                df["Miete"] = df['Miete'].str.replace(" €","")
                df["Miete"] = df['Miete'].str.replace("€","")
                df[["Miete", "Größe"]] = df[["Miete", "Größe"]].astype(float)
                df["Lease term"] = df["frei bis"] - df["frei ab"]
                #print(df.columns)
                #print(df["Lease term"])

                # Create two date objects
                date1 = pd.to_datetime('2022-03-20')
                date2 = pd.to_datetime('2022-03-25')

                # Calculate the difference between the two dates
                diff = date2 - date1

                # Print the difference in days
                #print(diff.days)


                df['Lease term'] = (df['frei bis'].dt.year - df['frei ab'].dt.year) * 12 + (df['frei bis'].dt.month - df['frei ab'].dt.month)

                df["EUR / SQM"] = df["Miete"] / df["Größe"]
                #print(df)
                return df

            def requestswg5():

                '''
                url = "https://www.wg-gesucht.de/1-zimmer-wohnungen-und-wohnungen-in-Berlin.8.1+2.0.0.html"

                # Add headers to mimic a browser request
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
                }

                response = requests.get(url, headers=headers)

                # check the status code of the response
                print(response.status_code)

                # access the content of the response
                html_content = response.content
                print(html_content)
                '''

                url1 = "https://www.wg-gesucht.de/1-zimmer-wohnungen-und-wohnungen-in-Berlin.8.1+2.0.0.html"
                url2 = "https://www.wg-gesucht.de/1-zimmer-wohnungen-und-wohnungen-in-Berlin.8.1+2.0.1.html?pagination=1&pu="
                url3 = "https://www.wg-gesucht.de/1-zimmer-wohnungen-und-wohnungen-in-Berlin.8.1+2.0.2.html?pagination=1&pu="
                url4 = "https://www.wg-gesucht.de/1-zimmer-wohnungen-und-wohnungen-in-Berlin.8.1+2.0.3.html?pagination=1&pu="
                url5 = "https://www.wg-gesucht.de/1-zimmer-wohnungen-und-wohnungen-in-Berlin.8.1+2.0.4.html?pagination=1&pu="


                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
                }
                response = requests.get(url5, headers=headers)

                dfs = pd.read_html(response.content)
                df = dfs[0]  # assuming the desired table is the first one on the page

                # Format the dataframe
                df['frei bis'] = pd.to_datetime(df['frei bis'], dayfirst=True)
                df['frei ab'] = pd.to_datetime(df['frei ab'], dayfirst=True)
                df["Größe"] = df['Größe'].str.replace("m²","")
                df["Miete"] = df['Miete'].str.replace(" €","")
                df["Miete"] = df['Miete'].str.replace("€","")
                df[["Miete", "Größe"]] = df[["Miete", "Größe"]].astype(float)
                df["Lease term"] = df["frei bis"] - df["frei ab"]
                #print(df.columns)
                #print(df["Lease term"])

                # Create two date objects
                date1 = pd.to_datetime('2022-03-20')
                date2 = pd.to_datetime('2022-03-25')

                # Calculate the difference between the two dates
                diff = date2 - date1

                # Print the difference in days
                #print(diff.days)


                df['Lease term'] = (df['frei bis'].dt.year - df['frei ab'].dt.year) * 12 + (df['frei bis'].dt.month - df['frei ab'].dt.month)

                df["EUR / SQM"] = df["Miete"] / df["Größe"]
                #print(df)
                return df

            #df1 = requestswg()
            #df2 = requestswg2()
            #df3 = requestswg3()
            #df4 = requestswg4()
            #df5 = requestswg5()

            #df_concat = pd.concat([df1, df2, df3, df4, df5])
            df_concat = requestswg_all()
            df_concat.dropna(subset=["Eintrag"], inplace=True)
            df_concat.reset_index(drop=True, inplace=True)

            #Give eachrow a name
            def combine_names(row):
                return str(row['Eintrag']) + '-' + str(row['Miete'])  + '-' + str(row['EUR / SQM']) + ' ' + str(row['Stadtteil'])

            df_concat['Name'] = df_concat.apply(combine_names, axis=1)

            #Cleaning out the neighbourhoods
            neighbourhoods = df_concat["Stadtteil"].unique()
            df_concat["Neighbourhood"] = ""

            neighbourhoods_list = ["Blankenburg", "Charlottenburg", "Friedrichshain", "Kreuzberg", "Mitte", "Moabit", "Neukölln", "Prenzlauer Berg"]
            neighbourhoods_clean = []
            neighbourhoods_dirty = df_concat["Stadtteil"].to_numpy().tolist()
            print(neighbourhoods_dirty)

            #Clean out neighbourhoods
            for neighbourhood in neighbourhoods_dirty:
                print(str(neighbourhood))

                if str(neighbourhood).__contains__("Altglienicke"):
                    print("Altglienicke")
                    neighbourhoods_clean.append("Altglienicke")

                elif str(neighbourhood).__contains__("Alt- Treptower"):
                    print("Alt- Treptower")
                    neighbourhoods_clean.append("Alt-Treptow")

                elif str(neighbourhood).__contains__("Blankenburg"):
                    print("Blankenburg")
                    neighbourhoods_clean.append("Blankenburg")

                elif str(neighbourhood).__contains__("Buch"):
                    print("Buch")
                    neighbourhoods_clean.append("Buch")

                elif str(neighbourhood).__contains__("Charlottenburg"):
                    print("Charlottenburg")
                    neighbourhoods_clean.append("Charlottenburg")

                elif str(neighbourhood).__contains__("Friedrichshain"):
                    print("Friedrichshain")
                    neighbourhoods_clean.append("Friedrichshain")

                elif str(neighbourhood).__contains__("Friedrischain"):
                    print("Friedrischain")
                    neighbourhoods_clean.append("Friedrichshain")

                elif str(neighbourhood).__contains__("Gesundbrunnen"):
                    print("Gesundbrunnen")
                    neighbourhoods_clean.append("Gesundbrunnen")

                elif str(neighbourhood).__contains__("Halensee"):
                    print("Halensee")
                    neighbourhoods_clean.append("Halensee")

                elif str(neighbourhood).__contains__("Hellersdorf"):
                    print("Hellersdorf")
                    neighbourhoods_clean.append("Hellersdorf")

                elif str(neighbourhood).__contains__("Hermsdorf"):
                    print("Hermsdorf")
                    neighbourhoods_clean.append("Hermsdorf")

                elif str(neighbourhood).__contains__("Karow"):
                    print("Karow")
                    neighbourhoods_clean.append("Karow")

                elif str(neighbourhood).__contains__("Karlshorst"):
                    print("Karlshorst")
                    neighbourhoods_clean.append("Karlshorst")

                elif str(neighbourhood).__contains__("Kleinmachnow"):
                    print("Kleinmachnow")
                    neighbourhoods_clean.append("Kleinmachnow")

                elif str(neighbourhood).__contains__("Kreuzberg"):
                    print("Kreuzberg")
                    neighbourhoods_clean.append("Kreuzberg")

                elif str(neighbourhood).__contains__("kreuzberg"):
                    print("kreuzberg")
                    neighbourhoods_clean.append("Kreuzberg")

                elif str(neighbourhood).__contains__("Köpenick"):
                    print("Köpenick")
                    neighbourhoods_clean.append("Köpenick")

                elif str(neighbourhood).__contains__("Lankwitz"):
                    print("Lankwitz")
                    neighbourhoods_clean.append("Lankwitz")

                elif str(neighbourhood).__contains__("Lichtenberg"):
                    print("Lichtenberg")
                    neighbourhoods_clean.append("Lichtenberg")

                elif str(neighbourhood).__contains__("Lichterfelde"):
                    print("Lichterfelde")
                    neighbourhoods_clean.append("Lichterfelde")

                elif str(neighbourhood).__contains__("Marienfelde"):
                    print("Mitte")
                    neighbourhoods_clean.append("Marienfelde")

                elif str(neighbourhood).__contains__("Mariendorf"):
                    print("Mariendorf")
                    neighbourhoods_clean.append("Mariendorf")

                elif str(neighbourhood).__contains__("Marzahn"):
                    print("Marzahn")
                    neighbourhoods_clean.append("Marzahn")

                elif str(neighbourhood).__contains__("mitte"):
                    print("mitte")
                    neighbourhoods_clean.append("Mitte")

                elif str(neighbourhood).__contains__("Mitte"):
                    print("Mitte")
                    neighbourhoods_clean.append("Mitte")

                elif str(neighbourhood).__contains__("Moabit"):
                    print("Moabit")
                    neighbourhoods_clean.append("Moabit")

                elif str(neighbourhood).__contains__("Neukölln"):
                    print("Neukölln")
                    neighbourhoods_clean.append("Neukölln")

                elif str(neighbourhood).__contains__("Nikolassee"):
                    print("Nikolassee")
                    neighbourhoods_clean.append("Nikolassee")

                elif str(neighbourhood).__contains__("Niederschönhausen"):
                    print("Niederschönhausen")
                    neighbourhoods_clean.append("Niederschönhausen")

                elif str(neighbourhood).__contains__("Oberschöneweide"):
                    print("Oberschöneweide")
                    neighbourhoods_clean.append("Oberschöneweide")

                elif str(neighbourhood).__contains__("Pankow"):
                    print("Pankow")
                    neighbourhoods_clean.append("Pankow")

                elif str(neighbourhood).__contains__("Prenzlauer Berg"):
                    print("Prenzlauer Berg")
                    neighbourhoods_clean.append("Prenzlauer Berg")

                elif str(neighbourhood).__contains__("Reinickendorf"):
                    print("Reinickendorf")
                    neighbourhoods_clean.append("Reinickendorf")

                elif str(neighbourhood).__contains__("Rummelsburg"):
                    print("Rummelsburg")
                    neighbourhoods_clean.append("Rummelsburg")

                elif str(neighbourhood).__contains__("Siemensstadt"):
                    print("Siemensstadt")
                    neighbourhoods_clean.append("Siemensstadt")

                elif str(neighbourhood).__contains__("Schillerkiez"):
                    print("Schillerkiez")
                    neighbourhoods_clean.append("Schillerkiez")

                elif str(neighbourhood).__contains__("Schmargendorf"):
                    print("Schmargendorf")
                    neighbourhoods_clean.append("Schmargendorf")

                elif str(neighbourhood).__contains__("Schöneberg"):
                    print("Schöneberg")
                    neighbourhoods_clean.append("Schöneberg")

                elif str(neighbourhood).__contains__("Spandau"):
                    print("Spandau")
                    neighbourhoods_clean.append("Spandau")

                elif str(neighbourhood).__contains__("spandau"):
                    print("spandau")
                    neighbourhoods_clean.append("Spandau")

                elif str(neighbourhood).__contains__("Steglitz"):
                    print("Steglitz")
                    neighbourhoods_clean.append("Steglitz")

                elif str(neighbourhood).__contains__("Steglitz-Zehlendorf"):
                    print("Steglitz-Zehlendorf")
                    neighbourhoods_clean.append("Steglitz-Zehlendorf")

                elif str(neighbourhood).__contains__("Tegel"):
                    print("Tegel")
                    neighbourhoods_clean.append("Tegel")

                elif str(neighbourhood).__contains__("Tiergarten"):
                    print("Tiergarten")
                    neighbourhoods_clean.append("Tiergarten")

                elif str(neighbourhood).__contains__("Tempelhof"):
                    print("Tempelhof")
                    neighbourhoods_clean.append("Tempelhof")

                elif str(neighbourhood).__contains__("Treptow"):
                    print("Treptow")
                    neighbourhoods_clean.append("Treptow")

                elif str(neighbourhood).__contains__("Wannsee"):
                    print("Wannsee")
                    neighbourhoods_clean.append("Wannsee")

                elif str(neighbourhood).__contains__("Wedding"):
                    print("Wedding")
                    neighbourhoods_clean.append("Wedding")

                elif str(neighbourhood).__contains__("wedding"):
                    print("wedding")
                    neighbourhoods_clean.append("Wedding")

                elif str(neighbourhood).__contains__("Weißensee"):
                    print("Weißensee")
                    neighbourhoods_clean.append("Weißensee")

                elif str(neighbourhood).__contains__("Wilmersdorf"):
                    print("Wilmersdorf")
                    neighbourhoods_clean.append("Wilmersdorf")

                elif str(neighbourhood).__contains__("Zehlendorf"):
                    print("Zehlendorf")
                    neighbourhoods_clean.append("Zehlendorf")

                else:
                    neighbourhoods_clean.append(("Berlin"))
            df_concat["Neighbourhood"] = neighbourhoods_clean

            #Get periods of end dates
            df_concat['frei bis (Year - Month)'] = pd.to_datetime(df_concat['frei bis']).dt.to_period('M')
            print(neighbourhoods_clean)

            #Get locations of each neighbourhood
            addresses = df_concat["Neighbourhood"].to_list()
            print(len(addresses))
            latitudes = []
            longitudes = []
            for location in addresses:
                try:
                    url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(location) +'?format=json'
                    response = requests.get(url).json()
                    print("Address: "+location)
                    print("latitude: "+response[0]["lat"])
                    print("longitude: "+response[0]["lon"])
                    latitudes.append(response[0]["lat"])
                    longitudes.append(response[0]["lon"])
                    print("Next...")
                except:
                    latitudes.append("Location not found: "+location)
                    longitudes.append("Location not found: "+location)
                    print("Location not found: "+location)
            df_concat["Latitude"] = latitudes
            df_concat["Longitude"] = longitudes

            #Export file
            if os.path.exists(nameofdataframe):
                st.write("Deleting existing csv output file")
                os.remove(nameofdataframe)
            else:
                st.write("No output file, continuing.")

            df_concat.to_csv(f"{nameofdataframe}")

            access_token = st.secrets.token
            repo_name = "wggesucht"
            g = Github(access_token)
            repo = g.get_user().get_repo(repo_name)
            csv_file = pd.read_csv(nameofdataframe)
            csv_file_string = csv_file.to_csv(index=False)
            csv_file_content = InputFileContent(csv_file_string)
            csv_file_content_str = str(csv_file_content)

            contents = repo.get_contents(nameofdataframe)

            repo.delete_file(nameofdataframe, "remove dataframe", contents.sha, branch="main")
            repo.create_file(nameofdataframe, "upload new dataframe", csv_file_string)
            st.write(f"Dataframe with name {nameofdataframe} uploaded.")
            # Notify the user that the file has been updated
            st.success(f"The file {nameofdataframe} has been updated!")
            button_pressed = False

            if button_pressed:
                st.write("Processing...")
            else:
                st.write("Ready to refresh again!")

        #Specify a path
        path = nameofdataframe
        # file modification timestamp of a file
        m_time = os.path.getctime(path)
        # convert timestamp into DateTime object
        dt_m = dt.datetime.fromtimestamp(m_time).strftime("%d/%m/%Y - %H:%M:%S")
        st.write(f'File last created on: {dt_m}')
        st.markdown("""---""")


    df_concat = pd.read_csv(nameofdataframe)
    st.markdown("""---""")

    with st.expander("Data cleaning and merging"):
        df_Ausschnitt_1_WE_Liste = pd.read_csv("Ambelin Case Study - Ausschnitt 1 WE-Liste.csv")
        df_Ausschnitt_2_WE_Liste = pd.read_csv("Ambelin Case Study - Ausschnitt 2 WE-Liste.csv")

        df_konditionen = pd.read_csv("Ambelin Case Study - Konditionen.csv")
        df_konditionen["Miete pro Monat"] = df_konditionen["Miete pro Monat"].map(lambda x: x.replace(',', ""))

        mark = ["x"]
        df_konditionen = df_konditionen[df_konditionen["Grundmiete"].isin(mark)]

        df_konditionen["Miete pro Monat"] = df_konditionen["Miete pro Monat"].astype(float)

        df_konditionen_pivot = df_konditionen.pivot_table(
            index="Mietobjektschlüssel",
            aggfunc={"Miete pro Monat":["sum"], "Wirtschaftseinheit":["unique"], "Mieteinheit":["unique"]})

        df_konditionen_pivot[["Wirtschaftseinheit", "Mieteinheit"]] = df_konditionen_pivot[["Wirtschaftseinheit", "Mieteinheit"]].astype(int)

        st.write(df_konditionen_pivot.columns)
        st.write(df_konditionen_pivot.columns[0])
        st.write(df_konditionen_pivot.columns[1])
        st.write(df_konditionen_pivot.columns[2])
        #st.write(df_konditionen_pivot.columns[3])
        columntorename = df_konditionen_pivot.columns[1]
        columntorename2 = df_konditionen_pivot.columns[2]
        #columntorename3 = df_konditionen_pivot.columns[3]
        st.write(str(columntorename))

        #df_konditionen_pivot.rename(columns={columntorename: 'Miete pro monat sum', str(columntorename2): "Mieteinheit", str(columntorename3): "Wirtschaftseinheit"}, inplace=True)
        st.write("Pivoted konditionen table")
        st.write(df_konditionen_pivot)
        st.write(len(df_konditionen_pivot))

        df_kontoauswertung = pd.read_csv("Ambelin Case Study - Kontoauswertung.csv")
        df_mos = pd.read_csv("Ambelin Case Study - MOS.csv")

        df_merge_mos_konditionen = pd.merge(
            df_mos, df_konditionen_pivot,
            how="left",
            left_on="Mietobjektschlüssel",
            right_on="Mietobjektschlüssel")
        st.write("Merged Mos & Konditionen")
        st.write(df_merge_mos_konditionen)
        st.write(len(df_merge_mos_konditionen))


        columntorename = df_merge_mos_konditionen.columns[3:4][0]
        columntorename2 = df_merge_mos_konditionen.columns[5:6][0]
        columntorename3 = df_merge_mos_konditionen.columns[4:5][0]
        df_merge_mos_konditionen.rename(columns={columntorename: 'Miete pro monat sum', columntorename2: "Wirtschaftseinheit", columntorename3: "Mieteinheit"}, inplace=True)

        st.write("Merged Mos & Konditionen renamed ")
        st.write(df_merge_mos_konditionen)
        st.write(len(df_merge_mos_konditionen))

        st.write("Merged Mos & Konditionen renamed columns")

        st.write(df_merge_mos_konditionen.columns)
        numberofmissinggrundmiete = df_merge_mos_konditionen['Miete pro monat sum'].isna().sum()
        st.write(f"Number of missing grundmiete: {numberofmissinggrundmiete}")

        df_we = pd.read_csv("Ambelin Case Study - WE.csv")

        df_merge_we_auschnitt1 = pd.merge(
            df_we, df_Ausschnitt_1_WE_Liste,
            how="inner",
            left_on="Wirtschaftseinheit",
            right_on="Wirtschaftseinheit")
        st.write("Merged WE & Aufschnitt1")

        st.write(df_merge_we_auschnitt1)
        st.write(len(df_merge_we_auschnitt1))

        df_merge_df_merge_we_auschnitt1_auschnitt2 = pd.merge(
            df_merge_we_auschnitt1, df_Ausschnitt_2_WE_Liste,
            how="left",
            left_on="Wirtschaftseinheit",
            right_on="Wirtschaftseinheit")
        df_merge_df_merge_we_auschnitt1_auschnitt2["Wirtschaftseinheit"] = df_merge_df_merge_we_auschnitt1_auschnitt2["Wirtschaftseinheit"].astype(int)
        st.write("Merged WE & Aufschnitt1 & Auschnitt 2")
        st.write(df_merge_df_merge_we_auschnitt1_auschnitt2)
        st.write(len(df_merge_df_merge_we_auschnitt1_auschnitt2))

        df_ambelin = pd.merge(
            df_merge_mos_konditionen, df_merge_df_merge_we_auschnitt1_auschnitt2,
            how="left",
            left_on="Mieteinheit",
            right_on="Wirtschaftseinheit"
        )
        df_ambelin["Miete pro monat sum"].fillna(0, inplace=True)
        st.write(df_ambelin)
        st.write(len(df_ambelin))


    #Filtering a bit more the dataframe
    dataframe_filter1 = df_concat["Größe"] > 9
    dataframe_filter2 = df_concat["Miete"] > 9
    df_concat = df_concat[dataframe_filter1]

    def add_logo():
        st.markdown(
            """
            <style>
                [data-testid="stSidebarNav"] {
                    background-image: url(https://github.com/christianheins/wggesucht/blob/main/images/ambelin%20Logo%20freigestellt%20dark%20blue.png?raw=true);
                    background-repeat: no-repeat;
                    background-size: contain;
                    background-position: center top;
                    padding-top: 110px;
                    text-align: center;
                    margin-top: -100px;

                }
                [data-testid="stSidebarNav"]::before {
                    content: "Pages";
                    margin-left: 20px;
                    margin-top: 20px;
                    font-size: 30px;
                    position: relative;
                    top: 100px;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )
    add_logo()

    col1, col2 = st.columns([0.2, 0.8])
    with col1:
        st.markdown("<a href='https://www.linkedin.com/in/christian-h-0545aaa1/'>🔗 Find me on LinkedIn</a>", unsafe_allow_html=True)
        st.markdown("<a href='https://github.com/christianheins'>🔗 Find me on Github</a>", unsafe_allow_html=True)
    with col2:
        with st.expander("INSTRUCTIONS"):
            st.markdown("<h6 style='text-align: left; color: red;'>Instructions</h6>", unsafe_allow_html=True)
            st.markdown(f"<li style='text-align: left; color: grey; font-size: 12px;'>This web applications is capturing a snapshot of the last months entries as of the date the csv file was lastly refreshed from here: 'https://www.wg-gesucht.de/1-zimmer-wohnungen-und-wohnungen-in-Berlin.8.1+2.0.0.html?pagination=1&pu='</li>", unsafe_allow_html=True)
            st.markdown(f"<li style='text-align: left; color: grey; font-size: 12px;'>Please use as a guide for only the WG Gesucht portal, this data is not completly representative. It's just an example of the powerful features Steramlit has to offer. Logos and images are WG Gesuchts property and not mine.</li>", unsafe_allow_html=True)

    if selected == "🏘️ Apartments":
        st.markdown("<h1 style='text-align: center; color: #17285B;'>🏘️ Property Analysis 🏘</h1>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns([0.3, 0.3, 0.3])
        with col1:
            numberofgrundmiete = df_ambelin[df_ambelin["Miete pro monat sum"]>0].count().loc["Miete pro monat sum"]
            st.metric("Number or Mietobjekte with Grundmiete above 0", value="{:,.0f}".format(numberofgrundmiete))
        with col2:
            st.metric("Number or Mietobjekte / Rental Keys without Grundmiete", value="{:,.0f}".format(numberofmissinggrundmiete))
        with col3:
            st.metric("Total number of Rental Properties",value="{:,.0f}".format(len(df_ambelin)))

        st.markdown(f"<h6 style='text-align: left; color: red;'>The number of missing values for a 'Grundmiete' or 'Wirtschaftseinheit' is {numberofmissinggrundmiete}. This is also presummably because not all grundmiete belong to certain financial accounts.</h6>", unsafe_allow_html=True)


        st.markdown("""---""")

        df_ambelin_filtered = df_ambelin[df_ambelin["Miete pro monat sum"]>0]

        df_concat = df_ambelin_filtered

        df_concat.rename(columns = {"Miete pro monat sum":"Miete"}, inplace=True)


        df_statistics = df_concat[["Miete"]].describe()
        st.markdown("<h3 style='text-align: left; color: #17285B;'>📊 A little bit of Descriptive Statistics</h3>", unsafe_allow_html=True)

        percent_25 = df_statistics.loc["25%"]["Miete"]
        percent_50 = df_statistics.loc["50%"]["Miete"]
        percent_75 = df_statistics.loc["75%"]["Miete"]


        # create bins for the price groups
        bins = [0, percent_25, percent_50, percent_75, float('inf')]

        # create labels for the price groups
        labels = ['Percent 25', 'Percent 50', 'Percent 75', 'Rest']

        # create a new column in the dataframe to hold the price group for each property
        df_concat['price_group'] = pd.cut(df_concat['Miete'], bins=bins, labels=labels)

        # print the dataframe
        #st.write(df_concat[["Miete", "price_group"]])

        df_price_groups = df_concat.pivot_table(index="price_group", values="Mietobjektschlüssel", aggfunc="count").reset_index()

        col1, col2, col3 = st.columns([0.2, 0.4, 0.4])

        with col1:
            st.metric("Average Grundmiete", value="{:,.0f} €".format(df_concat["Miete"].mean()))
            st.metric("Standard deviation rent", value="{:,.0f} €".format(df_concat["Miete"].std()))
            st.metric("Total Grundmiete", value="{:,.0f} €".format(df_concat["Miete"].sum()))
            st.metric("25% of the leases are up to", value="{:,.0f} €".format(percent_25))
            st.metric("50% of the leases are up to", value="{:,.0f} €".format(percent_50))
            st.metric("75% of the leases are up to", value="{:,.0f} €".format(percent_75))
            st.metric("Max rent", value="{:,.0f} €".format(df_concat["Miete"].max()))

        with col2:
            st.write(df_concat[["Miete"]].describe())
            st.markdown("""---""")

            chart = alt.Chart(df_concat.describe().reset_index()).encode(
                x=alt.X('Miete:Q'),
                y=alt.Y('index:N', sort=None), #use 'sort=None' to preserve the order of categories
                text=alt.Text('Miete', format='.1f')
            )
            #Combine bar chart with text chart, weird isnt?
            wholechart = alt.layer(chart.mark_bar(color="orange"), chart.mark_text(align='center', dy=-5, color="black"))

            st.altair_chart(wholechart.interactive(), use_container_width=True)

        with col3:
            chart = alt.Chart(df_price_groups).mark_arc(innerRadius=90).encode(
                theta='Mietobjektschlüssel:Q',
                color=alt.Color('price_group', scale=alt.Scale(scheme='category10')),
                tooltip=['Mietobjektschlüssel:Q'],
            )
            chart = chart.configure_legend(
                orient='right'
            )
            st.altair_chart(chart.interactive(), use_container_width=True)

            st.markdown("""---""")


            #st.write(df_price_groups)
            chart = alt.Chart(df_price_groups).encode(
                x=alt.X('Mietobjektschlüssel:Q'),
                y=alt.Y('price_group:N', sort=None), #use 'sort=None' to preserve the order of categories
                text=alt.Text('Mietobjektschlüssel', format='.1f')
            )
            #Combine bar chart with text chart, weird isnt?
            wholechart = alt.layer(chart.mark_bar(color="orange"), chart.mark_text(align='center', dy=-5, color="black"))

            st.altair_chart(wholechart.interactive(), use_container_width=True)


        with st.expander("Open for property table"):
            st.markdown("<h5 style='text-align: left; color: #17285B;'>Property Table</h5>", unsafe_allow_html=True)
            st.write(df_concat)


        st.markdown("""---""")
        st.markdown("<h3 style='text-align: left; color: #17285B;'>📈 Rent Timeline</h3>", unsafe_allow_html=True)

        df_concat_neighbourhoods = df_concat[['Rubrik', 'Eintrag', 'Miete', 'Größe', 'EUR / SQM', 'Stadtteil', 'Neighbourhood']].pivot_table(index="Neighbourhood", values="Eintrag", aggfunc="count").reset_index()
        df_concat_neighbourhoods.sort_values(by=["Eintrag"], ascending=[False], inplace=True)

        df_concat_endofleaseterm = df_concat[['Rubrik', 'Eintrag', 'Miete', 'Größe', 'EUR / SQM', 'Stadtteil', 'Neighbourhood', 'Lease term']].pivot_table(index="Lease term", values="Eintrag", aggfunc="count").reset_index()
        df_concat_endofleaseterm.sort_values(by=["Eintrag"], ascending=[False], inplace=True)

        col1, col2, col3= st.columns([0.3, 0.3, 0.3])
        with col1:
            df_concat_pivot_longterm = df_concat["Lease term"].isna().sum()
            df_concat_pivot_shortterm = len(df_concat[df_concat["Lease term"] > 0])
            source = pd.DataFrame({"Category": ["Indefinite term", "Limited term"], "Value": [df_concat_pivot_longterm, df_concat_pivot_shortterm]})
            st.markdown("<h6 style='text-align: center; color: orange;'>Lease term Donut</h6>", unsafe_allow_html=True)

            chart = alt.Chart(source).mark_arc(innerRadius=90).encode(
                theta='Value:Q',
                color=alt.Color('Category', scale=alt.Scale(scheme='category10')),
                tooltip=['Value:Q'],
            )
            chart = chart.configure_legend(
                orient='left'
            )
            st.altair_chart(chart.interactive(), use_container_width=True)

            st.markdown("<h6 style='text-align: center; color: orange;'>Lease term Bar Chart</h6>", unsafe_allow_html=True)
            chart = alt.Chart(df_concat_endofleaseterm).encode(
                x=alt.X('Lease term:Q'),
                y=alt.Y('Eintrag:Q', sort=None), #use 'sort=None' to preserve the order of categories
                text=alt.Text('Eintrag', format='.1f')
            )
            #Combine bar chart with text chart, weird isnt?
            wholechart = alt.layer(chart.mark_bar(color="orange"), chart.mark_text(align='center', dy=-5, color="black"))

            st.altair_chart(wholechart.interactive(), use_container_width=True)

        with col2:
            st.markdown("<h6 style='text-align: center; color: orange;'>Top 10 Neighbourhoods by count</h6>", unsafe_allow_html=True)

            df_concat_neighbourhoods_filtered = df_concat_neighbourhoods.iloc[:10]

            chart = alt.Chart(df_concat_neighbourhoods_filtered).mark_arc(innerRadius=90).encode(
                theta='Eintrag:Q',
                color=alt.Color('Neighbourhood', scale=alt.Scale(scheme='category10')),
                tooltip=['Neighbourhood', 'Eintrag:Q'],
            )

            chart = chart.configure_legend(
                orient='left'
            )
            st.altair_chart(chart.interactive(), use_container_width=True)

            df_concat_neighbourhoods_filtered = df_concat_neighbourhoods.iloc[:20]
            chart = alt.Chart(df_concat_neighbourhoods_filtered).encode(
                x=alt.X('Eintrag:Q'),
                y=alt.Y('Neighbourhood:N', sort=None), #use 'sort=None' to preserve the order of categories
                text=alt.Text('Eintrag:Q', format='.1f'),
            )
            #Combine bar chart with text chart, weird isnt?

            #wholechart = chart.mark_bar(color="orange") + chart.mark_text(align='left', dx=8, color="black")

            wholechart = alt.layer(chart.mark_bar(color="orange"), chart.mark_text(align='left', dx=8, color="black"))

            st.markdown("<h6 style='text-align: center; color: orange;'>Top 20 Neighbourhoods Bar Chart</h6>", unsafe_allow_html=True)
            st.altair_chart(wholechart.interactive(), use_container_width=True)

        with col3:
            st.markdown("<h6 style='text-align: center; color: orange;'>Release dates</h6>", unsafe_allow_html=True)
            chart = alt.Chart(source).mark_arc(innerRadius=90).encode(
                    theta='Value:Q',
                    color=alt.Color('Category', scale=alt.Scale(scheme='category10')),
                    tooltip=['Value:Q'],
                )
            chart = chart.configure_legend(
                orient='left'
            )
            st.altair_chart(chart.interactive(), use_container_width=True)
            df_concat_pivot_releasedate = df_concat[['Rubrik', 'Eintrag', 'Miete', 'Größe', 'EUR / SQM', 'Stadtteil', 'Neighbourhood']].pivot_table(index="Eintrag", values="Miete", aggfunc={"Miete":["count","mean"]}).reset_index()
            df_concat_pivot_releasedate['Eintrag'] = pd.to_datetime(df_concat_pivot_releasedate['Eintrag'], format='%d.%m.%Y', dayfirst=True)
            df_concat_pivot_releasedate.sort_values(by=["Eintrag"], ascending=[False], inplace=True)
            df_concat_pivot_releasedate['Eintrag'] = df_concat_pivot_releasedate['Eintrag'].dt.strftime('%Y/%m/%d')

            st.markdown("<h6 style='text-align: center; color: orange;'>Number of entries per release date</h6>", unsafe_allow_html=True)

            chart = alt.Chart(df_concat_pivot_releasedate).encode(
                x=alt.X('count:Q'),
                y=alt.Y('Eintrag:N', sort=None), #use 'sort=None' to preserve the order of categories
                text=alt.Text('count', format='.1f')
            )
            #Combine bar chart with text chart, weird isnt?

            #wholechart = chart.mark_bar(color="orange") + chart.mark_text(align='left', dx=8, color="black")

            wholechart = alt.layer(chart.mark_bar(color="orange"), chart.mark_text(align='left', dx=8, color="black"))

            st.altair_chart(wholechart.interactive(), use_container_width=True)

        st.markdown("<h6 style='text-align: center; color: orange;'>Properties table</h6>", unsafe_allow_html=True)
        st.write(df_concat[['Name', 'Rubrik', 'Eintrag', 'Miete', 'Größe', 'EUR / SQM', 'Stadtteil', 'Neighbourhood', 'frei ab', 'frei bis','frei bis (Year - Month)', 'Lease term', 'Latitude', 'Longitude']])

        st.markdown("""---""")
        st.markdown("<h3 style='text-align: center; color: orange;'>Map of neighbourhoods</h6>", unsafe_allow_html=True)

        #df_concat.drop(df_concat[df_concat["Latitude"].str() != "Location not found: NA"], inplace=True)
        latitudes = ["Location not found: Wedding","Location not found: Reinickendorf","Location not found: Prenzlauer Berg","Location not found: Neukölln","Location not found: NA","Location not found: Moabit","Location not found: Mitte","Location not found: Marienfelde","Location not found: Lichtenberg","Location not found: Kreuzberg","Location not found: Charlottenburg"]
        df_concat = df_concat[~df_concat["Latitude"].isin(latitudes)]
        df_concat.rename(columns = {"Latitude":"lat","Longitude":"lon"}, inplace=True)
        df_concat['lat'] = pd.to_numeric(df_concat['lat'])
        df_concat['lon'] = pd.to_numeric(df_concat['lon'])
        st.map(df_concat)

        with st.container():
            st.write("This is inside the container")

            # You can call any Streamlit command, including custom components:
            st.bar_chart(np.random.randn(50, 3))

        st.write("This is outside the container")

    if selected == "🫂 Neighbourhoods":
        st.markdown("<h1 style='text-align: center; color: orange;'>Neighbourhood Analysis</h1>", unsafe_allow_html=True)
        st.write(df_concat)
        df_concat_pivot_neighbourhoods = df_concat.pivot_table(index="Neighbourhood", aggfunc={"Miete":["count","mean","sum"], "Größe":["count", "mean", "sum"]})
        st.write(df_concat_pivot_neighbourhoods)

    if selected == "📑 Sample contracts":
        st.markdown("<h1 style='text-align: center; color: orange;'>Neighbourhood Analysis</h1>", unsafe_allow_html=True)
        st.write(df_concat)
        df_concat_pivot_neighbourhoods = df_concat.pivot_table(index="Neighbourhood", aggfunc={"Miete":["count","mean","sum"], "Größe":["count", "mean", "sum"]})
        st.write(df_concat_pivot_neighbourhoods)



if __name__ == "__main__":
    main()
