import React, { useState } from 'react';
import { Heart, Sparkles } from 'lucide-react';
import MultiStepForm from './MultiStepForm';
import ProductInfoStep from './steps/ProductInfoStep';
import InfluencerInfoStep from './steps/InfluencerInfoStep';
import ResultsStep from './steps/ResultsStep';
import { FormData } from '../types';

// Validation function for ProductInfoStep
const validateProductInfo = (data: FormData): Record<string, string> | null => {
  const errors: Record<string, string> = {};
  if (!data.productName?.trim()) {
    errors.productName = 'Product name is required.';
  }
  if (!data.productDescription?.trim()) {
    errors.productDescription = 'Product description is required.';
  }
  if (!data.productPhotos || data.productPhotos.length === 0) {
    errors.productPhotos = 'Please upload at least one product photo.';
  }
  return Object.keys(errors).length > 0 ? errors : null;
};

const MatchingApp: React.FC = () => {
  const [formData, setFormData] = useState<FormData>({
    productName: '',
    productDescription: '',
    productPhotos: [],
    influencerName: '',
    influencerDescription: '',
    influencerContent: [],
    influencerStyle: '',
    influencerAudience: ''
  });

  const updateFormData = (newData: Partial<FormData>) => {
    setFormData(prevData => ({
      ...prevData,
      ...newData
    }));
  };

  const steps = [
    {
      id: 'product',
      title: 'Product Details',
      component: (
        <ProductInfoStep 
          formData={formData} 
          updateFormData={updateFormData} 
        />
      ),
      validate: validateProductInfo // Add validation function here
    },
    {
      id: 'influencer',
      title: 'Influencer Content',
      component: (
        <InfluencerInfoStep 
          formData={formData} 
          updateFormData={updateFormData} 
        />
      )
    },
    {
      id: 'results',
      title: 'Match Results',
      component: (
        <ResultsStep 
          formData={formData}
        />
      )
    }
  ];

  return (
    <div className="container mx-auto px-4 py-8 md:py-16">
      <div className="text-center mb-12">
        <div className="flex justify-center items-center mb-4">
          <Heart className="h-8 w-8 text-pink-500 mr-2" />
          <Sparkles className="h-8 w-8 text-purple-500" />
        </div>
        <h1 className="text-3xl md:text-4xl font-bold text-gray-800 mb-2">
          Brand Buddies
        </h1>
        <p className="text-gray-600 max-w-md mx-auto">
          Find the perfect fit between influencers and products with our intelligent matching platform.
        </p>
      </div>

      <div className="max-w-3xl mx-auto">
        {/* Pass formData to MultiStepForm */}
        <MultiStepForm steps={steps} formData={formData} />
      </div>
    </div>
  );
};

export default MatchingApp