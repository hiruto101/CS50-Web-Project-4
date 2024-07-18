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
function edit(id){
    const content = document.getElementById(`content-${id}`);
    const editbtn = document.getElementById(`editbtn-${id}`);
    const savebtn = document.getElementById(`savebtn-${id}`);

    // Hide Edit Button show Save Button
    editbtn.hidden = true;
    savebtn.hidden = false;

    // Set textarea to active
    content.disabled = false;
    content.autofocus = true;
    content.focus(); // CSS style
    content.setSelectionRange(content.innerHTML.length, content.innerHTML.length);

}


function save(id) {
    const content = document.getElementById(`content-${id}`);
    const editbtn = document.getElementById(`editbtn-${id}`);
    const savebtn = document.getElementById(`savebtn-${id}`);

    // Hide Save Button show Edit Button
    content.blur();
    editbtn.hidden = false;
    savebtn.hidden = true;
    content.disabled = true;

    // Set the New Value
    const post = content.value;

        fetch(`/edit/${id}`,{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFTOKEN': csrftoken
        },
        body: JSON.stringify({
            content: post
        })
        })
        .then(response => response.json())
        .then(data => {
        console.log(data);
        content.innerHTML= post;
        })
        .catch(error => {
        console.error(error);
        });
};

function del_post(id) {


    
}
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


function follow(id) {

    fetch(`/follow/${id}`,{
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFTOKEN': csrftoken
        },
        body: JSON.stringify({
            id: id
        })     
    })
    .then(response => response.json())
    .then(data => {

            const unfollowbtn = document.querySelector('.btn-unfollow')
            const followbtn = document.querySelector('.btn-follow')
            const follower_count = document.getElementById('follower-count')

            unfollowbtn.hidden = false;
            followbtn.hidden = true;
            follower_count.innerHTML = data.followers
   

    })
    .catch(error => {
        console.error(error);
    })
}


function unfollow(id) {

    fetch(`/unfollow/${id}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFTOKEN': csrftoken
        },
        body: JSON.stringify({
            id: id
        })
    })
    .then(response => response.json())
    .then(data => {

        // Get
        const unfollowbtn = document.querySelector('.btn-unfollow')
        const followbtn = document.querySelector('.btn-follow')
        const follower_count = document.getElementById('follower-count')
        // Modify
        unfollowbtn.hidden = true;
        followbtn.hidden = false;
        follower_count.innerHTML = data.followers

    })
    .catch(error => {
        console.error(error)
    })
}



// TEST FUNCTIONS //
// document.addEventListener('DOMContentLoaded', () => {

//     const likebtns = document.getElementsByClassName('btntest')
//     console.log("lenght", likebtns.length)
//     if(likebtns.length > 0) {
//         for(let x = 0; x < likebtns.length; x++) {
//             btn = likebtns[x]
//             btn.addEventListener('click', function() {
//                 console.log(this.dataset.postId)
//                 console.log("hello", x)
//             })
//         }

//     }
//     else {
//         console.log("no buttons")
//     }
// });