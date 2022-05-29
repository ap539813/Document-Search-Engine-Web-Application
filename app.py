import os
try:
    """Try to import the libraries first"""
    import altair as alt
    import streamlit as st
    # from subprocess import call
    import seaborn as sns
    import matplotlib.pyplot as plt

    import pickle

    # from bokeh.models.widgets import Button
    # from bokeh.models import CustomJS
    # from streamlit_bokeh_events import streamlit_bokeh_events

    from weblibrary_support import make_model_library
    from remoterepo_support import make_model_remoterepo
    from localrepo_support import make_model_localrepo
    from weblink_support import make_model_weblinks
    from configure_source import update_source
    from utils import MakeQuery


except:
    """If faced with any error it will try to setup the environment"""
    os.system('python set_up.py')




## Basic setup and app layout
st.set_page_config(layout="wide")

alt.renderers.set_embed_options(scaleFactor=2)

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 
results = {}
print('revisited!!')


# @st.cache
if __name__ == '__main__':
    with open('app_mode_status/mode.txt') as file:
        mode = file.read()

    operation_mode = st.sidebar.selectbox(
        "Mode of operation",
        ("Search", "Configure")
    )

    if operation_mode != 'None':
        mode = operation_mode

    if mode == 'Search':
        loc_res = {}
        rem_res = {}
        st.markdown("# Document search application")

        # stt_button = Button(label="Speak", width=100)

        # stt_button.js_on_event("button_click", CustomJS(code="""
        #     var recognition = new webkitSpeechRecognition();
        #     recognition.continuous = true;
        #     recognition.interimResults = true;
        
        #     recognition.onresult = function (e) {
        #         var value = "";
        #         for (var i = e.resultIndex; i < e.results.length; ++i) {
        #             if (e.results[i].isFinal) {
        #                 value += e.results[i][0].transcript;
        #             }
        #         }
        #         if ( value != "") {
        #             document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
        #         }
        #     }
        #     recognition.start();
            
        #     """))

        # result = streamlit_bokeh_events(
        #     stt_button,
        #     events="GET_TEXT",
        #     key="listen",
        #     refresh_on_update=False,
        #     override_height=75,
        #     debounce_time=0)

        # # st.write(result)
        # if result:
        #     if "GET_TEXT" in result:
        #         st.write('search text:  ' + result.get("GET_TEXT"))
        #         query = result.get("GET_TEXT")

        # else:
        query = st.text_input("Enput the keyword")
        b = st.button('Search All')
        col1, col2 = st.columns(2)
        col3, col4 = st.columns(2)
        col1.markdown("#### Files from web libraries")
        col2.markdown("#### Files from web links")
        col3.markdown("#### Files from local repo")
        col4.markdown("#### Files from remote repo")
        b1 = col1.button("web libraries")
        b2 = col2.button("web links")
        b3 = col3.button("local repo")
        b4 = col4.button("remote repo")

        a_file = open("pickels/data.pkl", "rb")
        results = pickle.load(a_file)
        a_file.close()
        
        # st.write(results)
        try:
            if results['library'] != []:
                for item in results['library']:
                    if item['Score'] != None:
                        # link_file = item['Subject']
                        # file_found = f"{item['Subject']}"
                        col1.success(f"{item['Subject']}")
                        # with open(file_found, "rb") as file:
                        #     btn = col1.download_button(
                        #         label='open local file',
                        #         data=file,
                        #         file_name=file_found,
                        #         mime=None)

            if results['weblinks'] != []:
                for item in results['weblinks']:
                    if item['Score'] != None:
                        col2.success(f"{item['Subject']}")
                        # file_found = f"{item['Subject']}"
                        # with open(file_found, "rb") as file:
                        #     btn = col2.download_button(
                        #         label='open local file',
                        #         data=file,
                        #         file_name=file_found,
                        #         mime=None)

            if results['local'] != []:
                for item in results['local']:
                    if item['Score'] != None:
                        file_found = f"{item['Subject']}"
                        col3.success(item['Subject'])
                        with open(file_found, "rb") as file:
                            btn = col3.download_button(
                                label='open local file',
                                data=file,
                                file_name=file_found,
                                mime=None)

            if results['remote'] != []:
                for item in results['remote']:
                    if item['Score'] != None:
                        file_found = f"{item['Subject']}"
                        col4.success(item['Subject'])
                        with open(file_found, "rb") as file:
                            btn = col4.download_button(
                                label='open remote file',
                                data=file,
                                file_name=file_found,
                                mime=None)

        except Exception as e:
            st.write(e)
            # results = {}
            pass  

        if b1 or b:
            traineddata, Tfidmodel, df_news, vocabulary = make_model_library()
            if query != '':
                results['library'] = MakeQuery(query, vocabulary, df_news, traineddata)
                if not b:
                    for key in results:
                        if key != 'library':
                            results[key] = []
                cnt_files = 0
                # col1.write(results['library'])
                for item in results['library']:
                    if item['Score'] != None:
                        link_file = item['Subject']
                        col1.success(f"{item['Subject']}")
                        cnt_files += 1
                if cnt_files == 0:
                    col1.error('### No documents matching your request')

        if b2 or b:
            # query_weblinks()
            traineddata, Tfidmodel, df_news, vocabulary = make_model_weblinks()
            if query != '':
                results['weblinks'] = MakeQuery(query, vocabulary, df_news, traineddata)
                if not b:
                    for key in results:
                        if key != 'weblinks':
                            results[key] = []
                cnt_files = 0
                # col2.write(results['weblinks'])
                for item in results['weblinks']:
                    if (item['Score'] != None) and (item['Score'] > 0):
                        link_file = item['Subject']
                        col2.success(f"{item['Subject']}")
                        cnt_files += 1
                if cnt_files == 0:
                    col2.error('### No documents matching your request')
        if b3 or b:
            loc_res = {}
            traineddata, Tfidmodel, df_news, vocabulary = make_model_localrepo()
            if query != '':
                results['local'] = MakeQuery(query, vocabulary, df_news, traineddata)
                if not b:
                    for key in results:
                        if key != 'local':
                            results[key] = []
                cnt_files = 0
                for item in results['local']:
                    if item['Score'] != None:
                        loc_res[item['Subject']] = '' + item['Subject']
                        col3.success(item['Subject'])
                        with open(loc_res[item['Subject']], "rb") as file:
                            try:
                                btn = col3.download_button(
                                    label='open local file',
                                    data=file,
                                    file_name=loc_res[item['Subject']],
                                    mime=None)
                            except:
                                pass
                        
                        cnt_files += 1

                if cnt_files == 0:
                    col3.error('### No documents matching your request')
        if b4 or b:
            rem_res = {}
            traineddata, Tfidmodel, df_news, vocabulary = make_model_remoterepo()
            if query != '':
                results['remote'] = MakeQuery(query, vocabulary, df_news, traineddata)
                if not b:
                    for key in results:
                        if key != 'remote':
                            results[key] = []
                cnt_files = 0
                for item in results['remote']:
                    if item['Score'] != None:
                        with col4.container():
                            rem_res[item['Subject']] = '' + item['Subject']
                            col4.success(item['Subject'])
                            with open(rem_res[item['Subject']], "rb") as file:
                                try:
                                    btn = col4.download_button(
                                        label='open remote file',
                                        data=file,
                                        file_name=rem_res[item['Subject']],
                                        mime=None)
                                except:
                                    pass
                            cnt_files += 1
                if cnt_files == 0:
                    col4.error('### No documents matching your request')

        a_file = open("pickels/data.pkl", "wb")
        pickle.dump(results, a_file)
        a_file.close()
        with open('app_mode_status/mode.txt', 'w') as file:
            file.write(mode)

        print(results)
        st.sidebar.markdown('### The proportion of the result from various resources')
        fig, ax = plt.subplots()
        sns.barplot(x = list(results.keys()), y = [len(results[item]) for item in results], ax = ax)
        st.sidebar.pyplot(fig)
            
        
    else:
        type_data = st.selectbox('Select resource type',
                             ('web library', 'web link', 'local', 'remote'))

        resource_type = ['None', 'web library', 'web link', 'local', 'remote']

        path = st.text_input("Type in the path of the resource")

        submit = st.button('Insert')

        if submit:
            update_source(path = path, type_data = resource_type.index(type_data))

        with open('app_mode_status/mode.txt', 'w') as file:
            file.write(mode)
