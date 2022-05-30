// API Endpoints / URLs
const Root_URL = 'http://127.0.0.1:8000/'
const followingPostsURL = Root_URL + 'api/posts/following/page=1/'

const FollowingPosts = () => {
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
        getPaginatedPosts(followingPostsURL)
        }, [])
   
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


const App = () => {
    return (
        <div id='main-page'>
            <FollowingPosts />
        </div>
    )
}

ReactDOM.render(<App />, document.getElementById('app'))