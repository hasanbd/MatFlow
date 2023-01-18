import streamlit as st
import streamlit.components.v1 as components

def form():
    st.markdown(
    '''
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65" crossorigin="anonymous">

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-kenU1KFdBIe4zVF0s0G1M5b4hcpxyD9F7jL+jjXkk+Q2h455rYXK/7HAuoJl+0I4" crossorigin="anonymous"></script>
        <style>
          .contact .info-box {
          color: #444444;
          background: #fafbff;
          padding: 30px;
        }

        .contact .info-box i {
          font-size: 38px;
          line-height: 0;
          color: #4154f1;
        }

        .contact .info-box h3 {
          font-size: 20px;
          color: #012970;
          font-weight: 700;
          margin: 20px 0 10px 0;
        }

        .contact .info-box p {
          padding: 0;
          line-height: 24px;
          font-size: 14px;
          margin-bottom: 0;
        }
        </style>
      <section id="contact" class="contact">
        <div class="container" data-aos="fade-up">
          <header class="section-header">
            <h2>Contact Us</h2>
          </header>
          <div class="row gy-12">
            <div class="col-lg-12">
              <div class="row gy-12">
                <div class="col-md-6">
                  <div class="info-box">
                    <i class="bi bi-geo-alt"></i>
                    <h3>Address</h3>
                    <p>A108 Adam Street,<br>New York, NY 535022</p>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="info-box">
                    <i class="bi bi-telephone"></i>
                    <h3>Call Us</h3>
                    <p>+1 5589 55488 55<br>+1 6678 254445 41</p>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="info-box">
                    <i class="bi bi-envelope"></i>
                    <h3>Email Us</h3>
                    <p>info@example.com<br>contact@example.com</p>
                  </div>
                </div>
                <div class="col-md-6">
                  <div class="info-box">
                    <i class="bi bi-clock"></i>
                    <h3>Open Hours</h3>
                    <p>Monday - Friday<br>9:00AM - 05:00PM</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    ''', unsafe_allow_html=True
)   