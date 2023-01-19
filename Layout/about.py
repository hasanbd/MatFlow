import streamlit as st
import streamlit.components.v1 as components

def load_view():
    st.markdown(
    '''        
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65" crossorigin="anonymous">

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-kenU1KFdBIe4zVF0s0G1M5b4hcpxyD9F7jL+jjXkk+Q2h455rYXK/7HAuoJl+0I4" crossorigin="anonymous"></script>
        <style>
            .services .service-box {
            box-shadow: 0px 0 30px rgba(1, 41, 112, 0.08);
            height: 100%;
            padding: 60px 30px;
            text-align: center;
            transition: 0.3s;
            border-radius: 5px;
          }
          .services .service-box .icon {
            font-size: 36px;
            padding: 40px 20px;
            border-radius: 4px;
            position: relative;
            margin-bottom: 25px;
            display: inline-block;
            line-height: 0;
            transition: 0.3s;
          }
          .services .service-box h3 {
            color: #444444;
            font-weight: 700;
          }
          .services .service-box .read-more {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-weight: 600;
            font-size: 16px;
            padding: 8px 20px;
          }

          .services .service-box .read-more i {
            line-height: 0;
            margin-left: 5px;
            font-size: 18px;
          }

          .services .service-box.blue {
            border-bottom: 3px solid #2db6fa;
          }

          .services .service-box.blue .icon {
            color: #2db6fa;
            background: #dbf3fe;
          }

          .services .service-box.blue .read-more {
            color: #2db6fa;
          }

          .services .service-box.blue:hover {
            background: #2db6fa;
          }

          .services .service-box.orange {
            border-bottom: 3px solid #f68c09;
          }

          .services .service-box.orange .icon {
            color: #f68c09;
            background: #fde3c4;
          }

          .services .service-box.orange .read-more {
            color: #f68c09;
          }

          .services .service-box.orange:hover {
            background: #f68c09;
          }

          .services .service-box.green {
            border-bottom: 3px solid #08da4e;
          }

          .services .service-box.green .icon {
            color: #08da4e;
            background: #cffddf;
          }

          .services .service-box.green .read-more {
            color: #08da4e;
          }

          .services .service-box.green:hover {
            background: #08da4e;
          }

          .services .service-box.red {
            border-bottom: 3px solid #e9222c;
          }

          .services .service-box.red .icon {
            color: #e9222c;
            background: #fef7f8;
          }

          .services .service-box.red .read-more {
            color: #e9222c;
          }

          .services .service-box.red:hover {
            background: #e9222c;
          }

          .services .service-box.purple {
            border-bottom: 3px solid #b50edf;
          }

          .services .service-box.purple .icon {
            color: #b50edf;
            background: #f8e4fd;
          }

          .services .service-box.purple .read-more {
            color: #b50edf;
          }

          .services .service-box.purple:hover {
            background: #b50edf;
          }

          .services .service-box.pink {
            border-bottom: 3px solid #f51f9c;
          }

          .services .service-box.pink .icon {
            color: #f51f9c;
            background: #feecf7;
          }

          .services .service-box.pink .read-more {
            color: #f51f9c;
          }

          .services .service-box.pink:hover {
            background: #f51f9c;
          }

          .services .service-box:hover h3,
          .services .service-box:hover p,
          .services .service-box:hover .read-more {
            color: #fff;
          }

          .services .service-box:hover .icon {
            background: #fff;
          }
        </style>
        <section id="about" class="about">
            <div class="container" data-aos="fade-up">
                <div class="row gx-0">
                <div class="col-lg-6 d-flex flex-column justify-content-center" data-aos="fade-up" data-aos-delay="200">
                    <div class="content" style='background-color: #f6f9ff; padding: 40px;'>
                    <h3 style='font-size: 14px;font-weight: 700;color:#4154f1; text-transform: uppercase'>Who We Are</h3>
                    <h2 style='font-size: 24px;font-weight: 700;color: #012970;'>Expedita voluptas omnis cupiditate totam eveniet nobis sint iste. Dolores est repellat corrupti reprehenderit.</h2>
                    <p style='margin: 15px 0 30px 0;line-height: 24px;'>
                        Quisquam vel ut sint cum eos hic dolores aperiam. Sed deserunt et. Inventore et et dolor consequatur itaque ut voluptate sed et. Magnam nam ipsum tenetur suscipit voluptatum nam et est corrupti.
                    </p>
                    <div class="text-center text-lg-start">
                        <a href="#" class="btn btn-outline-sencondary d-inline-flex align-items-center justify-content-center align-self-center" style='line-height: 0;padding: 15px 40px;border-radius: 4px;transition: 0.5s;color: #fff;background: #4154f1;box-shadow: 0px 5px 25px rgba(65, 84, 241, 0.3);'>
                        <span style='font-family: "Nunito", sans-serif;font-weight: 600;font-size: 16px;letter-spacing: 1px;'>Read More</span>
                        <i class="bi bi-arrow-right" style='margin-left: 5px;font-size: 18px;transition: 0.3s;'></i>
                        </a>
                    </div>
                    </div>
                </div>
                <div class="col-lg-6 d-flex align-items-center" data-aos="zoom-out" data-aos-delay="200">
                    <img src="../assets/about.jpg" class="img-fluid" alt="">
                </div>
                </div>
            </div>
        </section>
        <div class="row feature-icons" data-aos="fade-up" style='margin-top: 120px;'>
          <h3 style='color: #012970;font-weight: 700;font-size: 32px;margin-bottom: 20px;text-align: center;'>Ratione mollitia eos ab laudantium rerum beatae quo</h3>
          <div class="row gy-4">
          <div class="col-lg-4 col-md-6" data-aos="fade-up" data-aos-delay="200">
            <div class="service-box blue" style='box-shadow: 0px 0 30px rgba(1, 41, 112, 0.08);height: 100%;padding: 60px 30px;text-align: center;transition: 0.3s;border-radius: 5px;border-bottom: 3px solid #2db6fa;'>
              <i class="ri-discuss-line icon" style='font-size: 36px;padding: 40px 20px;border-radius: 4px;position: relative;margin-bottom: 25px;display: inline-block;line-height: 0;transition: 0.3s;color: #2db6fa;
            background: #dbf3fe;'></i>
              <h3 style='color: #444444;
            font-weight: 700;'>Nesciunt Mete</h3>
              <p>Provident nihil minus qui consequatur non omnis maiores. Eos accusantium minus dolores iure perferendis tempore et consequatur.</p>
              <a href="#" class="read-more" style='display: inline-flex;
            align-items: center;
            justify-content: center;
            font-weight: 600;
            font-size: 16px;
            padding: 8px 20px;color: #2db6fa;'><span>Read More</span> <i class="bi bi-arrow-right" style='line-height: 0;
            margin-left: 5px;
            font-size: 18px;'></i></a>
            </div>
          </div>
        </div>
    ''', unsafe_allow_html=True
    )
