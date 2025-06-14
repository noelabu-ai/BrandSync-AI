import React from 'react';
import { PackageOpen } from 'lucide-react';
import FileUpload from '../common/FileUpload';
import { FormData } from '../../types';

interface ProductInfoStepProps {
  formData: FormData;
  updateFormData: (data: Partial<FormData>) => void;
  errors?: Record<string, string> | null; // Add errors prop
}

const ProductInfoStep: React.FC<ProductInfoStepProps> = ({ formData, updateFormData, errors }) => {
  const handleProductPhotosChange = (files: File[]) => {
    updateFormData({ productPhotos: files });
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-center py-4">
        <div className="bg-purple-100 p-3 rounded-full">
          <PackageOpen className="h-8 w-8 text-purple-600" />
        </div>
      </div>
      
      <h3 className="text-lg font-medium text-center text-gray-800">
        Tell us about your product
      </h3>
      
      <div className="space-y-4">
        <div>
          <label htmlFor="productName" className="block text-sm font-medium text-gray-700 mb-1">
            Product Name
          </label>
          <input
            id="productName"
            type="text"
            value={formData.productName}
            onChange={(e) => updateFormData({ productName: e.target.value })}
            placeholder="e.g. Organic Aloe Vera Moisturizer"
            className={`w-full px-4 py-2 border ${errors?.productName ? 'border-red-500' : 'border-gray-300'} rounded-lg focus:ring-2 ${errors?.productName ? 'focus:ring-red-500' : 'focus:ring-purple-500'} focus:border-transparent transition-colors duration-200`}
            required
          />
          {errors?.productName && (
            <p className="mt-1 text-xs text-red-600">{errors.productName}</p>
          )}
        </div>
        
        <div>
          <label htmlFor="productDescription" className="block text-sm font-medium text-gray-700 mb-1">
            Product Description
          </label>
          <textarea
            id="productDescription"
            value={formData.productDescription}
            onChange={(e) => updateFormData({ productDescription: e.target.value })}
            placeholder="Describe your product in a few sentences..."
            rows={4}
            className={`w-full px-4 py-2 border ${errors?.productDescription ? 'border-red-500' : 'border-gray-300'} rounded-lg focus:ring-2 ${errors?.productDescription ? 'focus:ring-red-500' : 'focus:ring-purple-500'} focus:border-transparent transition-colors duration-200 resize-none`}
            required
          />
          {errors?.productDescription && (
            <p className="mt-1 text-xs text-red-600">{errors.productDescription}</p>
          )}
        </div>
        
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Product Photos
          </label>
          <FileUpload
            onFilesSelected={handleProductPhotosChange}
            maxFiles={5}
            acceptedFileTypes="image/*"
            existingFiles={formData.productPhotos}
          />
          {errors?.productPhotos && (
            <p className="mt-1 text-xs text-red-600">{errors.productPhotos}</p>
          )}
          <p className="mt-2 text-xs text-gray-500">
            Upload up to 5 high-quality photos that showcase your product.
          </p>
        </div>
      </div>
    </div>
  );
};

export default ProductInfoStep;