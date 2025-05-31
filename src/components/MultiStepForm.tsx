import React, { useState } from 'react';
import FormNavigation from './common/FormNavigation';
import ProgressBar from './common/ProgressBar';
import { FormData } from '../types'; // Assuming FormData type definition

// Updated Step interface to include an optional validate function
interface Step {
  id: string;
  title: string;
  component: React.ReactNode; // This is expected to be a React Element, e.g., <ProductInfoStep .../>
  validate?: (formData: FormData) => Record<string, string> | null;
}

// Updated MultiStepFormProps to include formData
interface MultiStepFormProps {
  steps: Step[];
  formData: FormData;
}

const MultiStepForm: React.FC<MultiStepFormProps> = ({ steps, formData }) => {
  const [currentStepIndex, setCurrentStepIndex] = useState(0);
  const [direction, setDirection] = useState<'forward' | 'backward'>('forward');
  const [transitioning, setTransitioning] = useState(false);
  const [errors, setErrors] = useState<Record<string, string> | null>(null); // State for validation errors

  const goToNextStep = () => {
    setErrors(null); // Clear previous errors before attempting to navigate

    const currentStepDefinition = steps[currentStepIndex];
    if (currentStepDefinition.validate) {
      const validationErrors = currentStepDefinition.validate(formData);
      if (validationErrors && Object.keys(validationErrors).length > 0) {
        setErrors(validationErrors);
        return; // Stop navigation if there are errors
      }
    }

    if (currentStepIndex < steps.length - 1) {
      setTransitioning(true);
      setDirection('forward');
      setTimeout(() => {
        setCurrentStepIndex(currentStepIndex + 1);
        setTransitioning(false);
      }, 300);
    }
  };

  const goToPreviousStep = () => {
    setErrors(null); // Clear errors when going back
    if (currentStepIndex > 0) {
      setTransitioning(true);
      setDirection('backward');
      setTimeout(() => {
        setCurrentStepIndex(currentStepIndex - 1);
        setTransitioning(false);
      }, 300);
    }
  };

  const currentStep = steps[currentStepIndex];
  const progress = ((currentStepIndex) / (steps.length - 1)) * 100;
  
  const slideClass = transitioning
    ? direction === 'forward'
      ? 'translate-x-full opacity-0'
      : '-translate-x-full opacity-0'
    : 'translate-x-0 opacity-100';

  return (
    <div className="bg-white rounded-xl shadow-xl overflow-hidden">
      <div className="p-6 border-b border-gray-100">
        <h2 className="text-xl font-semibold text-gray-800 mb-1">
          {currentStep.title}
        </h2>
        <ProgressBar progress={progress} />
      </div>

      <div className="overflow-hidden relative">
        <div 
          className={`transition-all duration-300 ease-in-out transform ${slideClass}`}
        >
          <div className="p-6">
            {/* Render the (potentially cloned) step component */}
            {(() => {
              let componentToRender = currentStep.component;
              if (React.isValidElement(currentStep.component)) {
                // Ensure errors is always passed, even if null
                componentToRender = React.cloneElement(currentStep.component as React.ReactElement, { errors });
              }
              return componentToRender;
            })()}
          </div>
        </div>
      </div>

      <FormNavigation
        currentStepIndex={currentStepIndex}
        totalSteps={steps.length}
        onNext={goToNextStep}
        onPrevious={goToPreviousStep}
      />
    </div>
  );
};

export default MultiStepForm;