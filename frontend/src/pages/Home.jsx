import { Link } from 'react-router-dom'

const Home = () => {
  return (
    <div className="space-y-12">
      <section className="text-center py-12">
        <h1 className="text-4xl md:text-5xl font-bold mb-4">AI Content Creation Platform</h1>
        <p className="text-xl text-gray-600 max-w-3xl mx-auto">
          Create professional ads, social media content, and videos with the power of artificial intelligence.
        </p>
        <div className="mt-8 flex flex-wrap justify-center gap-4">
          <Link to="/ad-generation" className="btn btn-primary">Create Ads</Link>
          <Link to="/social-content" className="btn btn-primary">Generate Social Content</Link>
          <Link to="/video-generation" className="btn btn-primary">Create Videos</Link>
        </div>
      </section>
      
      <section className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="card text-center">
          <div className="bg-primary-100 text-primary-700 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5.882V19.24a1.76 1.76 0 01-3.417.592l-2.147-6.15M18 13a3 3 0 100-6M5.436 13.683A4.001 4.001 0 017 6h1.832c4.1 0 7.625-1.234 9.168-3v14c-1.543-1.766-5.067-3-9.168-3H7a3.988 3.988 0 01-1.564-.317z" />
            </svg>
          </div>
          <h3 className="text-xl font-semibold mb-2">Ad Generation</h3>
          <p className="text-gray-600">
            Create compelling ad copy for your products and services in seconds.
          </p>
          <Link to="/ad-generation" className="mt-4 inline-block text-primary-600 hover:underline">
            Get Started →
          </Link>
        </div>
        
        <div className="card text-center">
          <div className="bg-primary-100 text-primary-700 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 8h10M7 12h4m1 8l-4-4H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-3l-4 4z" />
            </svg>
          </div>
          <h3 className="text-xl font-semibold mb-2">Social Media Content</h3>
          <p className="text-gray-600">
            Generate engaging posts for all your social media platforms.
          </p>
          <Link to="/social-content" className="mt-4 inline-block text-primary-600 hover:underline">
            Get Started →
          </Link>
        </div>
        
        <div className="card text-center">
          <div className="bg-primary-100 text-primary-700 rounded-full w-16 h-16 flex items-center justify-center mx-auto mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" />
            </svg>
          </div>
          <h3 className="text-xl font-semibold mb-2">Video Generation</h3>
          <p className="text-gray-600">
            Create professional videos with AI-generated scripts and voiceovers.
          </p>
          <Link to="/video-generation" className="mt-4 inline-block text-primary-600 hover:underline">
            Get Started →
          </Link>
        </div>
      </section>
      
      <section className="bg-gray-100 p-8 rounded-lg">
        <h2 className="text-3xl font-bold mb-6 text-center">How It Works</h2>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="text-center">
            <div className="bg-white rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-4 shadow-md">
              <span className="text-xl font-bold text-primary-600">1</span>
            </div>
            <h3 className="font-semibold mb-2">Choose Content Type</h3>
            <p className="text-gray-600">Select the type of content you want to create.</p>
          </div>
          
          <div className="text-center">
            <div className="bg-white rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-4 shadow-md">
              <span className="text-xl font-bold text-primary-600">2</span>
            </div>
            <h3 className="font-semibold mb-2">Enter Details</h3>
            <p className="text-gray-600">Provide information about your brand and content needs.</p>
          </div>
          
          <div className="text-center">
            <div className="bg-white rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-4 shadow-md">
              <span className="text-xl font-bold text-primary-600">3</span>
            </div>
            <h3 className="font-semibold mb-2">Generate Content</h3>
            <p className="text-gray-600">Our AI creates high-quality content based on your inputs.</p>
          </div>
          
          <div className="text-center">
            <div className="bg-white rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-4 shadow-md">
              <span className="text-xl font-bold text-primary-600">4</span>
            </div>
            <h3 className="font-semibold mb-2">Use or Edit</h3>
            <p className="text-gray-600">Use the content as-is or make adjustments as needed.</p>
          </div>
        </div>
      </section>
    </div>
  )
}

export default Home
