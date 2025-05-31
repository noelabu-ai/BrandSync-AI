import React, { useState } from 'react';
import FormNavigation from './common/FormNavigation';
import ProgressBar from './common/ProgressBar';

interface Step {
  id: string;
  title: string;
  component: React.ReactNode;
}

interface MultiStepFormProps {
  steps: Step[];
}

const MultiStepForm: React.FC<MultiStepFormProps> = ({ steps }) => {
  const [currentStepIndex, setCurrentStepIndex] = useState(0);
  const [direction, setDirection] = useState<'forward' | 'backward'>('forward');
  const [transitioning, setTransitioning] = useState(false);

  const goToNextStep = () => {
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
            {currentStep.component}
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