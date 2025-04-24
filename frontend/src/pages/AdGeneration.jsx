import { useState } from 'react'
import { generateAd } from '../api/adService'

const AdGeneration = () => {
  const [formData, setFormData] = useState({
    brand_name: '',
    product_name: '',
    target_audience: '',
    key_features: '',
    tone: 'professional'
  })
  
  const [adCopy, setAdCopy] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  
  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }
  
  const handleSubmit = async (e) => {
    e.preventDefault()
    setIsLoading(true)
    setError('')
    
    try {
      // Convert key_features from comma-separated string to array
      const key_features_array = formData.key_features
        .split(',')
        .map(feature => feature.trim())
        .filter(feature => feature !== '')
      
      const response = await generateAd({
        ...formData,
        key_features: key_features_array
      })
      
      setAdCopy(response.ad_copy)
    } catch (err) {
      setError('Failed to generate ad. Please try again.')
      console.error(err)
    } finally {
      setIsLoading(false)
    }
  }
  
  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">AI Ad Generation</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div>
          <div className="card">
            <h2 className="text-xl font-semibold mb-4">Create Your Ad</h2>
            
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label htmlFor="brand_name" className="block text-sm font-medium text-gray-700 mb-1">
                  Brand Name
                </label>
                <input
                  type="text"
                  id="brand_name"
                  name="brand_name"
                  value={formData.brand_name}
                  onChange={handleChange}
                  className="input-field"
                  required
                />
              </div>
              
              <div>
                <label htmlFor="product_name" className="block text-sm font-medium text-gray-700 mb-1">
                  Product Name
                </label>
                <input
                  type="text"
                  id="product_name"
                  name="product_name"
                  value={formData.product_name}
                  onChange={handleChange}
                  className="input-field"
                  required
                />
              </div>
              
              <div>
                <label htmlFor="target_audience" className="block text-sm font-medium text-gray-700 mb-1">
                  Target Audience
                </label>
                <input
                  type="text"
                  id="target_audience"
                  name="target_audience"
                  value={formData.target_audience}
                  onChange={handleChange}
                  className="input-field"
                  required
                  placeholder="e.g., Young professionals, Parents, etc."
                />
              </div>
              
              <div>
                <label htmlFor="key_features" className="block text-sm font-medium text-gray-700 mb-1">
                  Key Features (comma-separated)
                </label>
                <textarea
                  id="key_features"
                  name="key_features"
                  value={formData.key_features}
                  onChange={handleChange}
                  className="input-field"
                  required
                  rows="3"
                  placeholder="e.g., Durable, Eco-friendly, Fast delivery"
                ></textarea>
              </div>
              
              <div>
                <label htmlFor="tone" className="block text-sm font-medium text-gray-700 mb-1">
                  Tone
                </label>
                <select
                  id="tone"
                  name="tone"
                  value={formData.tone}
                  onChange={handleChange}
                  className="input-field"
                  required
                >
                  <option value="professional">Professional</option>
                  <option value="friendly">Friendly</option>
                  <option value="humorous">Humorous</option>
                  <option value="formal">Formal</option>
                  <option value="casual">Casual</option>
                  <option value="enthusiastic">Enthusiastic</option>
                </select>
              </div>
              
              {error && (
                <div className="text-red-600 text-sm">{error}</div>
              )}
              
              <button
                type="submit"
                className="btn btn-primary w-full"
                disabled={isLoading}
              >
                {isLoading ? 'Generating...' : 'Generate Ad'}
              </button>
            </form>
          </div>
        </div>
        
        <div>
          <div className="card h-full">
            <h2 className="text-xl font-semibold mb-4">Generated Ad</h2>
            
            {isLoading ? (
              <div className="flex items-center justify-center h-64">
                <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-primary-600"></div>
              </div>
            ) : adCopy ? (
              <div className="bg-gray-50 p-4 rounded-md border border-gray-200 min-h-[300px]">
                <p className="whitespace-pre-line">{adCopy}</p>
                
                <div className="mt-6 flex justify-end">
                  <button
                    onClick={() => navigator.clipboard.writeText(adCopy)}
                    className="btn btn-secondary text-sm flex items-center"
                  >
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 5H6a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2v-1M8 5a2 2 0 002 2h2a2 2 0 002-2M8 5a2 2 0 012-2h2a2 2 0 012 2m0 0h2a2 2 0 012 2v3m2 4H10m0 0l3-3m-3 3l3 3" />
                    </svg>
                    Copy to Clipboard
                  </button>
                </div>
              </div>
            ) : (
              <div className="flex flex-col items-center justify-center h-64 text-gray-500">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 mb-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
                <p>Fill out the form and click "Generate Ad" to create your ad copy</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default AdGeneration
