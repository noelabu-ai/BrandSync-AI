import React from 'react';
import { ArrowLeft, ArrowRight } from 'lucide-react';

interface FormNavigationProps {
  currentStepIndex: number;
  totalSteps: number;
  onNext: () => void;
  onPrevious: () => void;
}

const FormNavigation: React.FC<FormNavigationProps> = ({
  currentStepIndex,
  totalSteps,
  onNext,
  onPrevious
}) => {
  const isFirstStep = currentStepIndex === 0;
  const isLastStep = currentStepIndex === totalSteps - 1;

  return (
    <div className="flex justify-between p-6 border-t border-gray-100">
      <button
        type="button"
        onClick={onPrevious}
        disabled={isFirstStep}
        className={`flex items-center px-4 py-2 rounded-lg transition-all duration-200 ${
          isFirstStep
            ? 'opacity-50 cursor-not-allowed text-gray-400'
            : 'hover:bg-gray-100 text-gray-700'
        }`}
      >
        <ArrowLeft className="h-4 w-4 mr-2" />
        Back
      </button>

      {!isLastStep && (
        <button
          type="button"
          onClick={onNext}
          className="flex items-center px-6 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors duration-200"
        >
          Next
          <ArrowRight className="h-4 w-4 ml-2" />
        </button>
      )}

      {isLastStep && (
        <button
          type="button"
          onClick={() => window.location.reload()}
          className="flex items-center px-6 py-2 bg-pink-500 text-white rounded-lg hover:bg-pink-600 transition-colors duration-200"
        >
          Start Over
        </button>
      )}
    </div>
  );
};

export default FormNavigation;