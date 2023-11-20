console.log("running")
fetch("/config/")
    .then((result) => { return result.json(); })
    .then((data) => {
        // Initialize Stripe.js
        const stripe = Stripe(data.publicKey);

        // new
        // Event handler
        //   document.querySelector("#submitBtn")
        document.querySelector("#payBtn").addEventListener("click", (event) => {
            // Get Checkout Session ID
            amount = document.getElementById('pay_amount').value
            console.log(amount)
            contract_id = event.target.value.toString()

            fetch("/create-checkout-session/" + contract_id + "?amount=" + amount)
                .then((result) => { return result.json(); })
                .then((data) => {

                    console.log('>>>', data.sessionId);
                    // Redirect to Stripe Checkout

                    return stripe.redirectToCheckout({ sessionId: data.sessionId })
                })
                .then((res) => {
                    console.log(res);
                });
        });
    });