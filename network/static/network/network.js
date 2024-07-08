function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');
//##################################CSRF TOKEN###############################################//

// EDIT FUNCTION
function edit(id) {
    const data1 = document.getElementById('test');
        fetch(`/edit/${id}`,{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFTOKEN': csrftoken
        },
        body: JSON.stringify({
            content:"content"
        })
        })
        .then(response => response.json())
        .then(data => {
        console.log(data);
        data1.innerHTML="Edit Load";
        })
        .catch(error => {
        console.error(error);
        });
};

// LIKE and UNLIKE Function
function like(id) {
    
    const likebtn = document.getElementById(`btn-like${id}`);
    const message = document.getElementById(`like-stat${id}`);
    let stat ='';
    
    for(const isLike of likebtn.classList) {
        if(isLike === 'like') {
            stat = 'like'
            likebtn.classList.remove('like');
            likebtn.classList.add('unlike');
        }
        else if(isLike === 'unlike') {
            stat = 'unlike'
            likebtn.classList.remove('unlike');
            likebtn.classList.add('like');
        }
    }
    
    const like_count = document.getElementById(`n_like${id}`)
    
    fetch(`/like/${id}`,{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFTOKEN': csrftoken
        },
        body: JSON.stringify({
            stat: stat
        })
    })
    .then(response => response.json())
    .then(data => {
        stat = data.message
        if(stat === 'liked') {
            console.log('like');
            like_count.innerHTML = data.likes;
            likebtn.innerHTML = " Unlike";
            likebtn.style.color = 'red';
        }
        else {
            console.log('unlike');
            like_count.innerHTML = data.likes;
            likebtn.innerHTML = " Like";
            likebtn.style.color = 'white';
        }
        
    })
    .catch(error => {
        console.error(error);
    });
};











// TEST FUNCTIONS //
document.addEventListener('DOMContentLoaded', () => {

    const likebtns = document.getElementsByClassName('btntest')
    console.log("lenght", likebtns.length)
    if(likebtns.length > 0) {
        for(let x = 0; x < likebtns.length; x++) {
            btn = likebtns[x]
            btn.addEventListener('click', function() {
                console.log(this.dataset.postId)
                console.log("hello", x)
            })
        }

    }
    else {
        console.log("no buttons")
    }
});