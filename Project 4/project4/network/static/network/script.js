console.log('js working.');

const Post = () => {
    return (
        <div className='post'>
            <span>Title</span>
            <span>User</span>
            <div>post content</div>
            <span>pub date</span>
        </div>
    )
}

const App = () => {
    return (
        <Post />
    )
}

ReactDOM.render(<App />, document.getElementById('app'))