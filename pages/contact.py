import streamlit as st
import streamlit.components.v1 as components

def form():
    components.html(
    """
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65" crossorigin="anonymous">

        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-kenU1KFdBIe4zVF0s0G1M5b4hcpxyD9F7jL+jjXkk+Q2h455rYXK/7HAuoJl+0I4" crossorigin="anonymous"></script>
        <form class="" style="margin-left: 100px; margin-right: 100px">
            <div class="form-group">
                <label for="exampleInputFirstName">First Name</label>
                <input type="email" class="form-control" id="exampleInputFirstName" aria-describedby="emailHelp" placeholder="Enter Your First Name">
            </div>
            <div class="form-group">
                <label for="exampleInputFirstName">Last Name</label>
                <input type="email" class="form-control" id="exampleInputFirstName" aria-describedby="emailHelp" placeholder="Enter Your Last Name">
            </div>
            <div class="form-group">
                <label for="exampleInputEmail1">Email address</label>
                <input type="email" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" placeholder="Enter email">
                <small id="emailHelp" class="form-text text-muted">We'll never share your email with anyone else.</small>
            </div>
            <div class="form-group">
                <label for="exampleInputFirstName">Last Name</label>
                <input as="textarea" rows="3" placeholder="Please provide as much detail as possible so we are able to better assist you" class="form-control" id="exampleInputFirstName" aria-describedby="emailHelp" placeholder="Enter Your Last Name">
            </div>
            <div class="form-check">
                <input type="checkbox" class="form-check-input" id="exampleCheck1">
                <label class="form-check-label" for="exampleCheck1">Check me out</label>
            </div>
            <button type="submit" class="btn btn-primary">Submit</button>
        </form>
    """
)