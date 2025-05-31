import { FormData } from '../types';

// This is a simplified "algorithm" for demo purposes
// In a real application, this would involve more sophisticated analysis
export const determineMatch = (formData: FormData) => {
  // Determine style compatibility based on product description and influencer style
  const styleCompatibility = calculateStyleCompatibility(formData);
  
  // Determine audience compatibility
  const audienceCompatibility = calculateAudienceCompatibility(formData);
  
  // Overall match score (weighted average)
  const score = Math.round((styleCompatibility * 0.6) + (audienceCompatibility * 0.4));
  
  // Determine if it's a match (over 70%)
  const isMatch = score >= 70;
  
  // Generate strengths and weaknesses
  const strengths = generateStrengths(formData, styleCompatibility, audienceCompatibility);
  const weaknesses = generateWeaknesses(formData, styleCompatibility, audienceCompatibility);
  
  return {
    isMatch,
    score,
    styleCompatibility,
    audienceCompatibility,
    strengths,
    weaknesses
  };
};

const calculateStyleCompatibility = (formData: FormData): number => {
  const { productDescription, influencerStyle } = formData;
  
  // This is a simplified version for demo purposes
  // A real implementation would use more sophisticated analysis
  let compatibility = 75; // Base compatibility
  
  // Adjust based on the influencer style and keywords in product description
  const productDescLower = productDescription.toLowerCase();
  
  // Style-specific adjustments
  switch (influencerStyle) {
    case "Minimalist":
      if (productDescLower.includes("simple") || 
          productDescLower.includes("clean") || 
          productDescLower.includes("minimal")) {
        compatibility += 20;
      } else if (productDescLower.includes("luxury") || 
                productDescLower.includes("ornate") || 
                productDescLower.includes("complex")) {
        compatibility -= 15;
      }
      break;
      
    case "Luxury/Premium":
      if (productDescLower.includes("premium") || 
          productDescLower.includes("luxury") || 
          productDescLower.includes("high-end")) {
        compatibility += 20;
      } else if (productDescLower.includes("budget") || 
                productDescLower.includes("affordable") || 
                productDescLower.includes("cheap")) {
        compatibility -= 15;
      }
      break;
      
    case "Natural/Organic":
      if (productDescLower.includes("organic") || 
          productDescLower.includes("natural") || 
          productDescLower.includes("eco")) {
        compatibility += 20;
      } else if (productDescLower.includes("synthetic") || 
                productDescLower.includes("artificial")) {
        compatibility -= 15;
      }
      break;
      
    case "Colorful/Vibrant":
      if (productDescLower.includes("vibrant") || 
          productDescLower.includes("colorful") || 
          productDescLower.includes("bright")) {
        compatibility += 20;
      } else if (productDescLower.includes("monochrome") || 
                productDescLower.includes("muted") || 
                productDescLower.includes("subtle")) {
        compatibility -= 10;
      }
      break;
  }
  
  // Number of photos as a signal of preparation
  const hasEnoughPhotos = formData.productPhotos.length >= 3;
  if (hasEnoughPhotos) {
    compatibility += 5;
  } else {
    compatibility -= 5;
  }
  
  // Clamp to 0-100 range
  return Math.max(0, Math.min(100, compatibility));
};

const calculateAudienceCompatibility = (formData: FormData): number => {
  const { productDescription, influencerAudience } = formData;
  
  // This is a simplified version for demo purposes
  let compatibility = 70; // Base compatibility
  
  // Audience-specific adjustments
  const productDescLower = productDescription.toLowerCase();
  
  switch (influencerAudience) {
    case "Gen Z":
      if (productDescLower.includes("trend") || 
          productDescLower.includes("young") || 
          productDescLower.includes("social media")) {
        compatibility += 25;
      } else if (productDescLower.includes("traditional") || 
                productDescLower.includes("classic") || 
                productDescLower.includes("mature")) {
        compatibility -= 15;
      }
      break;
      
    case "Millennials":
      if (productDescLower.includes("experience") || 
          productDescLower.includes("sustainable") || 
          productDescLower.includes("quality")) {
        compatibility += 25;
      }
      break;
      
    case "Beauty Lovers":
      if (productDescLower.includes("beauty") || 
          productDescLower.includes("cosmetic") || 
          productDescLower.includes("skincare")) {
        compatibility += 25;
      } else if (!(productDescLower.includes("appearance") || 
                  productDescLower.includes("look") || 
                  productDescLower.includes("skin"))) {
        compatibility -= 15;
      }
      break;
      
    case "Eco-Conscious":
      if (productDescLower.includes("sustainable") || 
          productDescLower.includes("eco") || 
          productDescLower.includes("green") ||
          productDescLower.includes("natural")) {
        compatibility += 25;
      } else if (productDescLower.includes("plastic") || 
                productDescLower.includes("disposable")) {
        compatibility -= 15;
      }
      break;
  }
  
  // Check influencer content volume
  const hasEnoughContent = formData.influencerContent.length >= 2;
  if (hasEnoughContent) {
    compatibility += 5;
  } else {
    compatibility -= 5;
  }
  
  // Clamp to 0-100 range
  return Math.max(0, Math.min(100, compatibility));
};

const generateStrengths = (
  formData: FormData, 
  styleCompatibility: number, 
  audienceCompatibility: number
): string[] => {
  const strengths: string[] = [];
  
  // Style strengths
  if (styleCompatibility > 80) {
    strengths.push(`The influencer's ${formData.influencerStyle} style perfectly complements your product's aesthetic.`);
  } else if (styleCompatibility > 60) {
    strengths.push(`The influencer's style has good potential to showcase your product effectively.`);
  }
  
  // Audience strengths
  if (audienceCompatibility > 80) {
    strengths.push(`Your product strongly appeals to the influencer's ${formData.influencerAudience} audience.`);
  } else if (audienceCompatibility > 60) {
    strengths.push(`There's good alignment between your product and the influencer's audience demographics.`);
  }
  
  // Content volume
  if (formData.influencerContent.length >= 3) {
    strengths.push("The influencer has provided multiple content examples, showing versatility.");
  }
  
  // Product presentation
  if (formData.productPhotos.length >= 3) {
    strengths.push("Your product is well-represented with multiple high-quality images.");
  }
  
  // Add generic strengths if we don't have enough
  if (strengths.length < 2) {
    strengths.push("The collaboration has potential to increase brand awareness.");
  }
  
  return strengths;
};

const generateWeaknesses = (
  formData: FormData, 
  styleCompatibility: number, 
  audienceCompatibility: number
): string[] => {
  const weaknesses: string[] = [];
  
  // Style weaknesses
  if (styleCompatibility < 50) {
    weaknesses.push(`The influencer's ${formData.influencerStyle} style may not be the best fit for your product presentation.`);
  } else if (styleCompatibility < 70) {
    weaknesses.push(`There are some style inconsistencies between the influencer and your product.`);
  }
  
  // Audience weaknesses
  if (audienceCompatibility < 50) {
    weaknesses.push(`Your product may not strongly resonate with the influencer's ${formData.influencerAudience} audience.`);
  } else if (audienceCompatibility < 70) {
    weaknesses.push(`There's room to improve alignment with the influencer's audience.`);
  }
  
  // Content volume
  if (formData.influencerContent.length < 2) {
    weaknesses.push("More content examples from the influencer would help assess compatibility better.");
  }
  
  // Product presentation
  if (formData.productPhotos.length < 2) {
    weaknesses.push("Additional product photos would improve the matching accuracy.");
  }
  
  // Add generic weakness if we don't have enough
  if (weaknesses.length < 2) {
    weaknesses.push("Consider providing more detailed information for more accurate matching.");
  }
  
  return weaknesses;
};