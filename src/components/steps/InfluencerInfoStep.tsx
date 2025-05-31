import React from 'react';
import { User } from 'lucide-react';
import FileUpload from '../common/FileUpload';
import { FormData } from '../../types';

interface InfluencerInfoStepProps {
  formData: FormData;
  updateFormData: (data: Partial<FormData>) => void;
}

const InfluencerInfoStep: React.FC<InfluencerInfoStepProps> = ({ formData, updateFormData }) => {
  const handleInfluencerContentChange = (files: File[]) => {
    updateFormData({ influencerContent: files });
  };

  const styleOptions = [
    "Minimalist",
    "Colorful/Vibrant",
    "Luxury/Premium",
    "Casual/Relaxed",
    "Artistic/Creative",
    "Professional/Corporate",
    "Vintage/Retro",
    "Natural/Organic",
    "Edgy/Alternative",
    "Playful/Fun"
  ];

  const audienceOptions = [
    "Gen Z",
    "Millennials",
    "Gen X",
    "Baby Boomers",
    "Fashion Enthusiasts",
    "Fitness & Wellness",
    "Beauty Lovers",
    "Tech Enthusiasts",
    "Foodies",
    "Travelers",
    "Eco-Conscious",
    "Luxury Shoppers"
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-center py-4">
        <div className="bg-pink-100 p-3 rounded-full">
          <User className="h-8 w-8 text-pink-600" />
        </div>
      </div>
      
      <h3 className="text-lg font-medium text-center text-gray-800">
        Tell us about the influencer
      </h3>
      
      <div className="space-y-4">
        <div>
          <label htmlFor="influencerName" className="block text-sm font-medium text-gray-700 mb-1">
            Influencer Name
          </label>
          <input
            id="influencerName"
            type="text"
            value={formData.influencerName}
            onChange={(e) => updateFormData({ influencerName: e.target.value })}
            placeholder="e.g. Jane Smith"
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-colors duration-200"
            required
          />
        </div>

        <div>
          <label htmlFor="influencerDescription" className="block text-sm font-medium text-gray-700 mb-1">
            Influencer Description
          </label>
          <textarea
            id="influencerDescription"
            value={formData.influencerDescription}
            onChange={(e) => updateFormData({ influencerDescription: e.target.value })}
            placeholder="Tell us about the influencer's niche, content style, and typical audience engagement..."
            rows={4}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-colors duration-200 resize-none"
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Influencer Content
          </label>
          <FileUpload
            onFilesSelected={handleInfluencerContentChange}
            maxFiles={5}
            acceptedFileTypes="image/*,video/*"
            existingFiles={formData.influencerContent}
          />
          <p className="mt-2 text-xs text-gray-500">
            Upload photos or videos that represent the influencer's style and content.
          </p>
        </div>

        <div>
          <label htmlFor="influencerStyle" className="block text-sm font-medium text-gray-700 mb-1">
            Influencer's Style
          </label>
          <select
            id="influencerStyle"
            value={formData.influencerStyle}
            onChange={(e) => updateFormData({ influencerStyle: e.target.value })}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-colors duration-200"
            required
          >
            <option value="" disabled>Select influencer's style</option>
            {styleOptions.map(style => (
              <option key={style} value={style}>{style}</option>
            ))}
          </select>
        </div>
        
        <div>
          <label htmlFor="influencerAudience" className="block text-sm font-medium text-gray-700 mb-1">
            Influencer's Primary Audience
          </label>
          <select
            id="influencerAudience"
            value={formData.influencerAudience}
            onChange={(e) => updateFormData({ influencerAudience: e.target.value })}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-colors duration-200"
            required
          >
            <option value="" disabled>Select primary audience</option>
            {audienceOptions.map(audience => (
              <option key={audience} value={audience}>{audience}</option>
            ))}
          </select>
        </div>
      </div>
    </div>
  );
};

export default InfluencerInfoStep;