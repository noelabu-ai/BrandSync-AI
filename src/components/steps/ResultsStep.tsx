import React, { useState, useEffect } from 'react';
import { CheckCircle, XCircle, Award, TrendingUp, Zap, Users } from 'lucide-react';
import { FormData } from '../../types';
import { determineMatch } from '../../utils/matchingAlgorithm';

interface ResultsStepProps {
  formData: FormData;
}

interface MatchResult {
  isMatch: boolean;
  score: number;
  styleCompatibility: number;
  audienceCompatibility: number;
  strengths: string[];
  weaknesses: string[];
}

const ResultsStep: React.FC<ResultsStepProps> = ({ formData }) => {
  const [result, setResult] = useState<MatchResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [showDetails, setShowDetails] = useState(false);

  useEffect(() => {
    // Simulate analysis with a delay
    const timer = setTimeout(() => {
      const matchResult = determineMatch(formData);
      setResult(matchResult);
      setLoading(false);
    }, 2500);

    return () => clearTimeout(timer);
  }, [formData]);

  if (loading) {
    return (
      <div className="py-12 text-center">
        <div className="flex justify-center mb-6">
          <div className="relative">
            <div className="w-16 h-16 border-4 border-purple-200 border-t-purple-600 rounded-full animate-spin"></div>
          </div>
        </div>
        <h3 className="text-lg font-medium text-gray-800 mb-2">
          Analyzing compatibility...
        </h3>
        <p className="text-gray-600">
          We're determining if this influencer is a good match for your product.
        </p>
      </div>
    );
  }

  if (!result) {
    return <div>Something went wrong. Please try again.</div>;
  }

  return (
    <div className="py-6">
      <div className="flex justify-center mb-6">
        {result.isMatch ? (
          <div className="bg-green-100 p-4 rounded-full">
            <CheckCircle className="h-12 w-12 text-green-600" />
          </div>
        ) : (
          <div className="bg-red-100 p-4 rounded-full">
            <XCircle className="h-12 w-12 text-red-600" />
          </div>
        )}
      </div>

      <h3 className="text-2xl font-bold text-center text-gray-800 mb-2">
        {result.isMatch ? "It's a Match!" : "Not a Strong Match"}
      </h3>
      
      <p className="text-center text-gray-600 mb-6">
        {result.isMatch
          ? "This influencer would be a great fit for your product based on our analysis."
          : "We think there might be better influencers for your product."}
      </p>

      <div className="mb-8">
        <div className="bg-gray-100 rounded-full h-4 mb-2">
          <div 
            className={`h-full rounded-full ${
              result.isMatch ? 'bg-gradient-to-r from-green-500 to-teal-500' : 'bg-gradient-to-r from-orange-500 to-red-500'
            }`}
            style={{ width: `${result.score}%` }}
          ></div>
        </div>
        <div className="flex justify-between text-xs text-gray-500">
          <span>Poor Match</span>
          <span>Perfect Match</span>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-4 mb-6">
        <div className="bg-purple-50 p-4 rounded-lg">
          <div className="flex items-center mb-2">
            <Zap className="h-4 w-4 text-purple-600 mr-2" />
            <h4 className="font-medium text-purple-800">Style Compatibility</h4>
          </div>
          <div className="text-2xl font-bold text-purple-900">
            {result.styleCompatibility}%
          </div>
        </div>
        
        <div className="bg-pink-50 p-4 rounded-lg">
          <div className="flex items-center mb-2">
            <Users className="h-4 w-4 text-pink-600 mr-2" />
            <h4 className="font-medium text-pink-800">Audience Alignment</h4>
          </div>
          <div className="text-2xl font-bold text-pink-900">
            {result.audienceCompatibility}%
          </div>
        </div>
      </div>

      <button 
        className="w-full py-2 text-sm text-purple-700 font-medium hover:text-purple-800 transition-colors duration-200 mb-6"
        onClick={() => setShowDetails(!showDetails)}
      >
        {showDetails ? "Hide Details" : "Show Details"}
      </button>

      {showDetails && (
        <div className="space-y-6 animate-fadeIn">
          <div>
            <h4 className="flex items-center text-sm font-medium text-gray-800 mb-2">
              <Award className="h-4 w-4 text-green-600 mr-2" />
              Strengths
            </h4>
            <ul className="space-y-2">
              {result.strengths.map((strength, index) => (
                <li key={index} className="flex items-start">
                  <CheckCircle className="h-4 w-4 text-green-500 mt-1 mr-2 flex-shrink-0" />
                  <span className="text-sm text-gray-700">{strength}</span>
                </li>
              ))}
            </ul>
          </div>

          <div>
            <h4 className="flex items-center text-sm font-medium text-gray-800 mb-2">
              <TrendingUp className="h-4 w-4 text-orange-600 mr-2" />
              Areas for Improvement
            </h4>
            <ul className="space-y-2">
              {result.weaknesses.map((weakness, index) => (
                <li key={index} className="flex items-start">
                  <XCircle className="h-4 w-4 text-orange-500 mt-1 mr-2 flex-shrink-0" />
                  <span className="text-sm text-gray-700">{weakness}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
};

export default ResultsStep;