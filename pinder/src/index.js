var TIMEOUT = 10;

function doAnwser(app, petme) {
    var answer = {
        petme: petme,
        img: app.cardSrc
    }

    axios.post('/api/doAnswer', answer)
        .then(function (response) {
            console.log(response);
        })
        .catch(function (error) {
            console.log(error);
        });

    app.cardSrc = "https://source.unsplash.com/collection/1424240/500x500?rand=" + Math.random();
    app.secs = 0;
    app.buttonsDisabled = true;
}

var app = new Vue({
    el: '#container',
    data: {
        message: 'Hello Vue!',
        timeout: TIMEOUT,
        secs: 0,
        buttonsDisabled: false,
        cardSrc: "https://source.unsplash.com/collection/1424240"
    },
    mounted: function () {
        window.setInterval(() => {
            this.secs++;
            this.buttonsDisabled = this.secs < TIMEOUT;
        }, 1000);
    },
    methods: {
        doYes: function () {
            console.log("Yay!");
            doAnwser(this, 1);
        },
        doNo: function () {
            console.log("Nay!");
            doAnwser(this, 0);
        }
    }
})