// API Endpoints / URLs
const Root_URL = 'http://127.0.0.1:8000/'
const allPostsURL = Root_URL + 'api/posts/all/page=1/'
const newPostURL = Root_URL + 'api/posts/new/'
const userStatusURL = Root_URL + 'api/user/status/'

// Helper functions

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

// Helper Functions end

const EditField = ({setCanEdit, setRerenderPosts, postID}) => {
    const editPostURL = Root_URL + `api/posts/${postID}/edit/`

    const [newPostContent, setNewPostContent] = React.useState('')

    const changePostValue = (event) => {
        setNewPostContent(event.target.value)
    }

    const submitPost = async () => {
        console.log('trying to submit a post.')
        console.log(`content: ${newPostContent}`)

        const response = await fetch(editPostURL, {
            method: 'PUT',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                'content': newPostContent,
            })
        })
        const data = await response.json()
        console.log(data)

        setCanEdit(false)
        setRerenderPosts('A post has been edited.')
    }

    const cancelEdit = () => {
        setCanEdit(false)
    }

    return (
        <div className='post-create-input'>
            <input type='text' id='post-content-field' value={newPostContent} onChange={changePostValue}></input>

            <div id='edit-field-btns'>
                <button id='post-edit-confirm-button' onClick={submitPost}> Confirm Changes </button>
                <button id='post-edit-cancel-button' onClick={cancelEdit}> Cancel </button>
            </div>
        </div>
    )
}

const Post = ({post, setRerenderPosts, userStatus}) => {
    const likeURL = Root_URL + `api/posts/${post.id}/like/`
    const unlikeURL = Root_URL + `api/posts/${post.id}/unlike/`
    const isPostLikedURL = Root_URL + `api/posts/${post.id}/likedby/requestuser/`
    const isPostOwnerURL = Root_URL + `api/posts/${post.id}/isowner/`
    const userProfileURL = Root_URL + `user/${post.user_id}/`

    const [isPostLiked, setIsPostLiked] = React.useState(false)
    const [isPostOwner, setIsPostOwner] = React.useState(false)
    const [canEdit, setCanEdit] = React.useState(false)

    React.useEffect(async () => {
        const isPostlikedResponse = await fetch(isPostLikedURL)
        const isPostlikedData = await isPostlikedResponse.json()

        const isPostOwnerResponse = await fetch(isPostOwnerURL)
        const isPostOwnerData = await isPostOwnerResponse.json()
        
        setIsPostLiked(isPostlikedData.is_post_liked_by_user)
        setIsPostOwner(isPostOwnerData.is_post_owner)
        // console.log(data)
    }, [canEdit])

    const likePost = async () => {
        const response = await fetch(likeURL, {
            method : 'PUT',
            headers: {
                'X-CSRFToken': csrftoken,
            },
        })
        const data = await response.json()

        // console.log(data)
        setRerenderPosts('A post has been liked')
        setIsPostLiked(true)
    }

    const unlikePost = async () => {
        const response = await fetch(unlikeURL, {
            method : 'PUT',
            headers: {
                'X-CSRFToken': csrftoken,
            },
        })
        const data = await response.json()
        // console.log(data)
        setRerenderPosts('A post has been unliked')
        setIsPostLiked(false)
    }

    const toggleEdit = () => {
        setCanEdit(true)
    }

    return (
        <div className='post'>
            <div className='post_content'>
                <div>{post.likes}</div>
                <span> <a href={userProfileURL}> {post.post_user} </a> </span>


                <div>
                    {

                        canEdit ?
                            <EditField setCanEdit={setCanEdit} postID={post.id} setRerenderPosts={setRerenderPosts}/>
                        :
                            <div>
                                {post.content}
                            </div>
                    }
                </div>

                <span>{post.date_published}</span>
            </div>

            {
                userStatus.authenticated &&
                    <div className='post_buttons'>
                        
                            {
                                isPostLiked ?
                                    <button onClick={unlikePost}> UnLike </button>
                                :
                                    <button onClick={likePost}> Like </button>
                            }

                            {
                                (isPostOwner && !canEdit ) &&
                                    <button onClick={toggleEdit}> Edit </button>
                            }
                    </div>
            }
        </div>
    )
}

const PostForm = ({setRerenderPosts}) => {
    const [postContent, setPostContent] = React.useState('')

    const changePostValue = (event) => {
        setPostContent(event.target.value)
    }

    const submitPost = async () => {
        console.log('trying to submit a post.')
        console.log(`content: ${postContent}`)

        const response = await fetch(newPostURL, {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            body: JSON.stringify({
                'content': postContent,
            })
        })

        setRerenderPosts('new post created.')
    }

    return (
        <div className='post-create-input'>
            <input type='text' id='post-content-field' value={postContent} onChange={changePostValue}></input>
            <button id='post-submit-button' onClick={submitPost}>Post</button>
        </div>
    )
}


const AllPosts = ({reRenderPosts, setRerenderPosts, userStatus}) => {
    const [postsObject, setPostsObject] = React.useState({})
    const [posts, setPosts] = React.useState({})

    const getPaginatedPosts = async (url) => {
        const response = await fetch(url)
        const data = await response.json()

        const postsArray = Object.values(data.posts)

        setPostsObject(data)
        setPosts(postsArray.reverse())
        // console.log(data)
    }

    React.useEffect(() => {
        getPaginatedPosts(allPostsURL)
        }, [reRenderPosts])
   
    return (
            <div class='post_container'>
                {
                    Object.keys(posts).map((post) => (
                        <Post post={posts[post]} setRerenderPosts={setRerenderPosts} userStatus={userStatus} />
                    ))

                    
                }

                {
                    (postsObject.has_previous) && <button onClick={() => {
                        getPaginatedPosts(postsObject.previous_page)
                    }}> Previous </button>
                }

                {
                    (postsObject.has_next) && <button onClick={() => {
                        getPaginatedPosts(postsObject.next_page)
                    }}> Next </button> 
                }
            </div>
    )
}


const App = () => {
    const [reRenderPosts, setRerenderPosts] = React.useState('')
    const [userStatus, setUserStatus] = React.useState({})

    React.useEffect(async () => {
        const response = await fetch(userStatusURL)
        const data = await response.json()

        // console.log(data)
        setUserStatus(data)
    }, [])

    return (
        <div id='main-page'>
            {
                userStatus.authenticated && <PostForm  setRerenderPosts={setRerenderPosts} />
            }

            <AllPosts reRenderPosts={reRenderPosts} setRerenderPosts={setRerenderPosts} userStatus={userStatus} />
        </div>
    )
}

ReactDOM.render(<App />, document.getElementById('app'))