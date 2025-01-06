import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import "./Dealers.css";
import "../assets/style.css";
import positive_icon from "../assets/positive.png"
import neutral_icon from "../assets/neutral.png"
import negative_icon from "../assets/negative.png"
import review_icon from "../assets/reviewbutton.png"
import Header from '../Header/Header';

const Dealer = () => {


    const [dealer, setDealer] = useState({});
    const [reviews, setReviews] = useState([]);
    const [unreviewed, setUnreviewed] = useState(false);
    const [postReview, setPostReview] = useState(<></>)

    let curr_url = window.location.href;
    let root_url = curr_url.substring(0, curr_url.indexOf("dealer"));
    let params = useParams();
    let id = params.id;
    let dealer_url = root_url + `djangoapp/dealer/${id}`;
    let reviews_url = root_url + `djangoapp/reviews/dealer/${id}`;
    let post_review = root_url + `postreview/${id}`;

    const get_dealer = async () => {
        try {
            const res = await fetch(dealer_url, {
                method: "GET"
            });
            const retobj = await res.json();
            console.log("Dealer API Response:", retobj);

            if (retobj.status === 200 && retobj.dealer) {
                // Assuming retobj.dealer is a single object, not an array
                setDealer(retobj.dealer);
            } else {
                console.error("Invalid dealer data:", retobj);
            }
        } catch (error) {
            console.error("Error fetching dealer:", error);
        }
    };


    const get_reviews = async () => {
        try {
            const res = await fetch(reviews_url, {
                method: "GET"
            });
            const retobj = await res.json();
            console.log("Reviews API Response:", retobj);

            if (retobj.status === 200 && Array.isArray(retobj.reviews)) {
                if (retobj.reviews.length > 0) {
                    setReviews(retobj.reviews);
                } else {
                    setUnreviewed(true);
                }
            } else {
                console.error("Invalid reviews data:", retobj);
            }
        } catch (error) {
            console.error("Error fetching reviews:", error);
        }
    };


    const senti_icon = (sentiment) => {
        let icon = sentiment === "positive" ? positive_icon : sentiment === "negative" ? negative_icon : neutral_icon;
        return icon;
    }

    useEffect(() => {
        get_dealer();
        get_reviews();
        if (sessionStorage.getItem("username")) {
            setPostReview(<a href={post_review}><img src={review_icon} style={{ width: '10%', marginLeft: '10px', marginTop: '10px' }} alt='Post Review' /></a>)


        }
    }, []);


    return (
        <div style={{ margin: "20px" }}>
            <Header />
            <div style={{ marginTop: "10px" }}>
                {dealer && dealer.full_name ? (
                    <>
                        <h1 style={{ color: "grey" }}>{dealer.full_name}{postReview}</h1>
                        <h4 style={{ color: "grey" }}>
                            {dealer['city']}, {dealer['address']}, Zip - {dealer['zip']}, {dealer['state']}
                        </h4>
                    </>
                ) : (
                    <p>Loading dealer information...</p>
                )}
            </div>
            <div className="reviews_panel">
                {reviews.length === 0 && unreviewed === false ? (
                    <p>Loading Reviews....</p>
                ) : unreviewed === true ? (
                    <div>No reviews yet! </div>
                ) : (
                    reviews.map(review => (
                        <div className='review_panel' key={review.id}>
                            <img src={senti_icon(review.sentiment)} className="emotion_icon" alt='Sentiment' />
                            <div className='review'>{review.review}</div>
                            <div className="reviewer">{review.name} {review.car_make} {review.car_model} {review.car_year}</div>
                        </div>
                    ))
                )}
            </div>
        </div>
    );

}

export default Dealer
