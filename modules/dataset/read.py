import base64

import streamlit as st

import pandas as pd
import glob

import time
# from modules import utils
import os
from shutil import rmtree
from PIL import Image
import sys

sys.path.append('./')
from code import DataExtraction, BuildDataset, ChartsForPaper
from io import StringIO
from pathlib import Path
def show_pdf(file_path):
    with open(file_path,"rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="800" height="800" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)

def show_all_graph():

    try:
        for i in st.session_state.graph:
            for k,j in i.items():
                st.caption(f"""<h4 style="font-size:1.5em;" > {k} </h4>""",unsafe_allow_html=True)
                st.pyplot(j)
    except:
        st.write('something went wrong')

def read_dataset(dataset):

    data = None
    # option_list = ["Upload File", "Github URL", "Manual Input", "Sample Data"]
    option_list = ["Upload File", "Sample Data"]

    option = st.radio(
        "File Upload Methods:",
        option_list,
        key="read_data_option",
        horizontal=True
    )

    col1, col2 = st.columns([7, 3])
    filepath_or_buffer = object
    if option == option_list[0]:
        path = Path().absolute()
        list_sample = {
            "Iris Dataset",
            "TMD Dataset",
            "Epsilon Dataset"
        }
        sample = col1.selectbox(
            "Select Dataset",
            list_sample,
            key=f"sample_data"
        )
        exp_name = sample
        filepath_or_buffer = upload_file()
        # return
    # elif option == option_list[1]:
    #	filepath_or_buffer = github_url(col1)
    # elif option == option_list[2]:
    #	filepath_or_buffer = manual_input(col1)
    elif option == option_list[1]:
        filepath = sample_data(col1)
        exp_name = filepath[0]
        filepath_or_buffer = filepath[1]

    name = col2.text_input(
        "Dataset Name",
        key=f"dataset_name"
    )

    # data ./ rawData / Deep4Chem / DB for chromophore_Sci_Data_rev02.csv  ./rawData/Deep4Chem/DoubleCheck-High Extinction.csv
    # dynamo './rawData/Dyomics/Dyomics_2017.pdf' './rawData/Dyomics/SmilesData.csv'
    # photo './rawData/PhotochemCAD3/PCAD3 Compd Database 2018/2018_03 PCAD3.db' './rawData/PhotochemCAD3/SmilesData.csv'
    # build './rawData/Experimental_SMILES_Predictions.csv'

    show_sample = col2.checkbox("Show Sample", key=f"show_sample")
    if show_sample:
        st.markdown('<h4>All raw datasets for DNA-Templated DYE aggregates</h4>', unsafe_allow_html=True)
        try:
            for i in filepath_or_buffer:
                x = i.rfind('\\')
                y = i.rfind('/')
                if x < y:
                    x = y
                x += 1
                with st.expander(i[x:]):
                    if i.endswith('.csv'):
                        dt = pd.read_csv(i)
                        st.table(dt.head())
        except:
            st.write('something went wrong')




            # split for showing last name



    uploaded_file = []

    if col1.button("Submit", key=f"read_submit") or st.session_state.call_fun:
        is_valid = validate(name, dataset.list_name())
        if is_valid:
            # st.session_state.dataset = filepath_or_buffer
            # st.session_state.experiment_name = exp_name
            base_name = exp_name.split(' ')[0]
            st.session_state.progress=0
            if base_name == 'Epsilon':
                pt = st.progress(st.session_state.progress)
                DataExtraction.run_all()
                if st.session_state.progress==0:
                    st.session_state.progress+=30
                pt.progress(st.session_state.progress)
                BuildDataset.run_all()
                if st.session_state.progress==30:
                    st.session_state.progress+=30
                pt.progress(st.session_state.progress)
                st.success("Success")
                if st.session_state.progress==60:
                    st.session_state.progress+=40
                if ChartsForPaper.run_all():
                    with st.expander('ML Visualization'):
                        show_all_graph()
                pt.progress(st.session_state.progress)
            # if data is not None:
            #     dataset.add(name, data)
            # else:
            #     try:
            #         for i in filepath_or_buffer:
            #             data = pd.read_csv(i)
            #             dataset.add(name, data)
            #             uploaded_file.append(data)
            #     except:
            #         pass
            #     if len(filepath_or_buffer)>1 or exp_name=='epsilon':
            #         print('hello')
            #         try:
            #             tab1,tab2=st.tabs(['Processing...','Result'])
            #             with tab1:
            #                 ## uncomment to make genarate output again ##
            #                 ## it will take too much time ##
            #                 # rmtree('output')
            #                 # os.mkdir('./output')
            #                 # print(uploaded_file)
            #                 # DataExtraction.deep4che(uploaded_file)
            #                 # print(uploaded_file)
            #                 # DataExtraction.dynamocs()
            #                 # DataExtraction.Photoche()
            #                 # DataExtraction.pubche()
            #                 BuildDataset.Experimental()
            #                 BuildDataset.Training()
            #                 BuildDataset.unknown()
            #                 # ChartsForPaper.prediction()
            #                 # ChartsForPaper.Ovall_RandomForest_Classifaications()
            #                 # ChartsForPaper.Ovall_RandomForestRegrassion()
            #                 # ChartsForPaper.Overall_Data()
            #
            #
            #         except Exception:
            #             st.error("Can't Process :( PLease try again.")
            # utils.rerun()


def upload_file():
    # pass
    # li={
    #     'DataExtraction':['deep4che','dynamocs','Photoche','pubche'],
    #     'BuildDataset':['Experimental','Training','unknown'],
    #     'ChartsForPaper':['Overall_Data','Ovall_RandomForest_Classifaications','prediction']
    # }
    # filepath_or_buffer={}
    # if exp_name=='epsilon':
    #     for i,j in li.items():
    #         for k in j:
    #             filepath_or_buffer[k]=col1.file_uploader(
    #                 "Choose a file for "+i+" "+k,
    #                 type=["csv"],
    #                 key=f"upload_file"+k
    #             )
    filepath_or_buffer = st.file_uploader('Upload dataset')
    if filepath_or_buffer:
        return filepath_or_buffer


# def github_url(col1):
#	filepath_or_buffer = col1.text_input(
#			"Github Raw Data URL",
#			key=f"github_url"
#		)

#	return filepath_or_buffer

# def manual_input(col1):
#	input_data = col1.text_area(
#			"Enter data in csv format",
#			key=f"manual_input_data"
#		)

#	if input_data:
#		filepath_or_buffer = StringIO(input_data)

#		return filepath_or_buffer

def sample_data(col1):
    path = Path().absolute()

    list_sample = {
        "Iris Dataset": [f"{path}/sample/iris.csv"],
        "TMD Dataset": [f"{path}/sample/tmd.csv"],
        "Epsilon Dataset": [
            f"{path}/rawData/Deep4Chem/DB for chromophore_Sci_Data_rev02.csv",
            f"{path}/rawData/Deep4Chem/DoubleCheck-High Extinction.csv",
            f"{path}/rawData/Dyomics/Dyomics_2017.pdf",
            f"{path}/rawData/Dyomics/SmilesData.csv",
            f"{path}/rawData/PhotochemCAD3/SmilesData.csv",
            f"{path}/rawData/Experimental_SMILES_Predictions.csv"
        ]
    }

    # data ./ rawData / Deep4Chem / DB for chromophore_Sci_Data_rev02.csv  ./rawData/Deep4Chem/DoubleCheck-High Extinction.csv
    # dynamo './rawData/Dyomics/Dyomics_2017.pdf' './rawData/Dyomics/SmilesData.csv'
    # photo './rawData/PhotochemCAD3/PCAD3 Compd Database 2018/2018_03 PCAD3.db' './rawData/PhotochemCAD3/SmilesData.csv'
    # build './rawData/Experimental_SMILES_Predictions.csv'

    sample = col1.selectbox(
        "Select Dataset",
        list_sample.keys(),
        key=f"sample_data"
    )

    return [sample, list_sample[sample]]


def validate(name, used_names):
    if name.strip() == "":  # check if name is empty string or only contains whitespace
        st.warning("Dataset name cannot be empty!")
        return False
    elif name in used_names:  # check if name is already used
        st.warning(f"Name {name} already used! Enter another name.")
        return False

    return True

# def read_dataset(dataset):
#     up=st.file_uploader('uploaded')
#     if st.button('submit'):
#         if 'val' not in st.session_state:
#             st.session_state.val=up
#         print(up)


# file_uploader=st.file_uploader('Upload files')
# if file_uploader is not None:
#     with open(os.path.join("./user_dummy", file_uploader.name), "wb") as f:
#         f.write(file_uploader.getbuffer())
#
# st.write('Your project')
# st.write('hello')
# projects=glob.glob(f'./user_dummy/*',recursive=True)
# if not projects:
#     st.write('No projects')
# else:
#     for p_names in projects:
#         if os.path.isfile(p_names):
#             continue
#         with st.expander(os.path.basename(p_names)):
#             for files in glob.glob(f'{p_names}/*',recursive=True):
#                 st.write(os.path.basename(files))
#             col1,col2=st.columns(2)
#             with col1:
#                 up=st.file_uploader('Upload file',key=os.path.basename(p_names)+'file')
#             with col2:
#                 name=st.text_input('Rename file',key=os.path.basename(p_names)+'rename')
#             btn=st.button('submit')
#             if btn:
#                 if up is not None:
#                     if name is not None and len(name)>0:
#                         up.name=name+'.csv'
#                     with open(os.path.join(p_names, up.name), "wb") as f:
#                         f.write(file_uploader.getbuffer())
#
# files=glob.glob(f'./user_dummy/*')
# st.write('Your files')
# if not files:
#     st.write('No files')
# else:
#     for i in files:
#         if os.path.isfile(i):
#             st.write(os.path.basename(i))
