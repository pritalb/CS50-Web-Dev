// API Endpoints / URLs
const Root_URL = 'http://127.0.0.1:8000/'
const allPostsURL = Root_URL + 'api/posts/all/page=1/'
// const newPostURL = Root_URL + 'api/posts/new/'
const newPostURL = 'http://127.0.0.1:8000/api/posts/new/'
// console.log(newPostURL)

const csrftoken = getCookie('csrftoken');
console.log(`csrf token: ${csrftoken}`)

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

// Helper Functions end

const Post = ({post}) => {
    return (
        <div className='post'>
            <h3>{post.likes}</h3>
            <span>{post.post_user}</span>
            <div>{post.content}</div>
            <span>{post.date_published}</span>
        </div>
    )
}

const AllPosts = ({reRenderPosts}) => {
    const [postsObject, setPostsObject] = React.useState({})
    const [posts, setPosts] = React.useState({})

    const getPaginatedPosts = async (url) => {
        const response = await fetch(url)
        const data = await response.json()

        const postsArray = Object.values(data.posts)

        setPostsObject(data)
        setPosts(postsArray.reverse())

        console.log(data)
    }

    React.useEffect(() => {
        getPaginatedPosts(allPostsURL)
        // console.log(posts)

        // const response = await fetch(url)
        // const data = await response.json()

        // const postsArray = Object.values(data.posts)

        // setPostsObject(data)
        // setPosts(postsArray.reverse())
        }, [reRenderPosts])
   
    return (
            <div class='post_container'>
                {
                    Object.keys(posts).map((post) => (
                        <Post post={posts[post]} />
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

const PostForm = ({setRerenderPosts}) => {
    const [postContent, setPostContent] = React.useState('')

    const changePostValue = (event) => {
        // console.log('value of content field changed')
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
            // credentials: 'same-origin',
            body: JSON.stringify({
                'content': postContent,
            })
        })

        setRerenderPosts('new post created.')
    }

    return (
        <div className='post-create-input'>
            <input type='text' id='post-content-field' value={postContent} onChange={changePostValue}></input>
            {/* <input type="hidden" name="csrfmiddlewaretoken" value={csrftoken}></input> */}
            <button id='post-submit-button' onClick={submitPost}>Post</button>
        </div>
    )
}

const App = () => {
    const [reRenderPosts, setRerenderPosts] = React.useState('')

    return (
        <div id='main-page'>
            <PostForm  setRerenderPosts={setRerenderPosts} />
            <AllPosts reRenderPosts={reRenderPosts} />
        </div>
    )
}

ReactDOM.render(<App />, document.getElementById('app'))