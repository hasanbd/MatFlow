import streamlit as st
import streamlit.components.v1 as components

def load_view():
    st.markdown(
    '''
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65" crossorigin="anonymous">

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-kenU1KFdBIe4zVF0s0G1M5b4hcpxyD9F7jL+jjXkk+Q2h455rYXK/7HAuoJl+0I4" crossorigin="anonymous"></script>
        <style>
            /*--------------------------------------------------------------
            # Footer
            --------------------------------------------------------------*/
            .footer .copyright {
            text-align: center;
            padding-top: 30px;
            color: #012970;
            }

            .footer .credits {
            padding-top: 10px;
            text-align: center;
            font-size: 13px;
            color: #012970;
            }
        </style>
        <footer id="footer" class="footer">
            <div class="container">
            <div>
                <h4 style='font-size: 20px;font-weight: 700;margin: 0 0 20px 0;color: #012970;'>Publications</h4>
                <p>
                    <span style='font-size: 16px;font-weight: 600;color: #012970;'>Austin Biaggne, Lawrence Spear, German Barcenas, Maia Ketteridge, Young C.Kim, Joseph S.Melinger, Willia B.Knowlton, Bernard Yurke, and Lan Li - </span>
                    <span class='text-muted'>Data-Driven and Multiscale Modeling of DNA-Templated Dye</span>   
                </p>
                <p>
                    <span style='font-size: 16px;font-weight: 600;color: #012970;'>Hasan M Jamil, Lan Li -</span>
                    <span class='text-muted'>A Knowledgebased Novel Materials Design System using Machine Learning</span>
                </p>
            </div>
            <div class="copyright">
                &copy; Copyright <strong><span>jamil@uidaho.edu</span></strong>. All Rights Reserved
            </div>
            </div>
        </footer>
''', unsafe_allow_html=True
)
