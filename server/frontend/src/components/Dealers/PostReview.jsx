import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import "./Dealers.css";
import "../assets/style.css";
import Header from '../Header/Header';

const PostReview = () => {
  const [dealer, setDealer] = useState({});
  const [review, setReview] = useState("");
  const [model, setModel] = useState("");
  const [year, setYear] = useState("");
  const [date, setDate] = useState("");
  const [carmodels, setCarmodels] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const params = useParams();
  const id = params.id;

  const rootUrl = window.location.origin + "/";
  const dealerUrl = `${rootUrl}djangoapp/dealer/${id}`;
  const reviewUrl = `${rootUrl}djangoapp/add_review`;
  const carmodelsUrl = `${rootUrl}djangoapp/get_cars`;

  const postReview = async () => {
    const name = sessionStorage.getItem("firstname") + " " + sessionStorage.getItem("lastname");
    const username = sessionStorage.getItem("username");
    const reviewerName = name.includes("null") ? username : name;

    if (!model || review === "" || date === "" || year === "") {
      alert("All fields are required!");
      return;
    }

    const [make, carModel] = model.split(" ");
    const reviewData = {
      name: reviewerName,
      dealership: id,
      review,
      purchase: true,
      purchase_date: date,
      car_make: make,
      car_model: carModel,
      car_year: year,
    };

    try {
      const response = await fetch(reviewUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(reviewData),
      });

      const result = await response.json();

      if (result.status === 200) {
        navigate(`/dealer/${id}`);
      } else {
        setError("Failed to submit the review. Please try again.");
      }
    } catch (err) {
      setError("An error occurred while submitting the review.");
    }
  };

  const fetchDealerDetails = async () => {
    try {
      const response = await fetch(dealerUrl);
      const data = await response.json();
      if (data.status === 200 && data.dealer.length > 0) {
        setDealer(data.dealer[0]);
      }
    } catch (err) {
      setError("Failed to load dealer details.");
    }
  };

  const fetchCarModels = async () => {
    try {
      setLoading(true);
      const response = await fetch(carmodelsUrl);
      const data = await response.json();
      setCarmodels(data.CarModels || []);
    } catch (err) {
      setError("Failed to load car models.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDealerDetails();
    fetchCarModels();
  }, []);

  return (
    <div>
      <Header />
      <div className="post-review-container" style={{ margin: "5%" }}>
        <h1 style={{ color: "darkblue" }}>{dealer.full_name || "Dealer Details"}</h1>

        {error && <p className="error-message">{error}</p>}

        <textarea
          id="review"
          cols="50"
          rows="7"
          placeholder="Write your review here..."
          onChange={(e) => setReview(e.target.value)}
        ></textarea>

        <div className="input_field">
          <label htmlFor="purchase-date">Purchase Date</label>
          <input
            type="date"
            id="purchase-date"
            onChange={(e) => setDate(e.target.value)}
            required
          />
        </div>

        <div className="input_field">
          <label htmlFor="cars">Car Make</label>
          <select
            name="cars"
            id="cars"
            onChange={(e) => setModel(e.target.value)}
            required
          >
            <option value="" disabled selected hidden>
              Choose Car Make and Model
            </option>
            {loading ? (
              <option>Loading...</option>
            ) : (
              carmodels.map((car, index) => (
                <option key={index} value={`${car.CarMake} ${car.CarModel}`}>
                  {car.CarMake} {car.CarModel}
                </option>
              ))
            )}
          </select>
        </div>

        <div className="input_field">
          <label htmlFor="car-year">Car Year</label>
          <br />
          <input
            type="number"
            id="car-year"
            onChange={(e) => setYear(e.target.value)}
            min={2015}
            max={2023}
            placeholder="Enter year (e.g., 2020)"
            required
          />
        </div>

        <div>
          <button className="postreview" onClick={postReview}>
            Post Review
          </button>
        </div>
      </div>
    </div>
  );
};

export default PostReview;
