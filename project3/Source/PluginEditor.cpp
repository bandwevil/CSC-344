/*
  ==============================================================================

  This is an automatically generated GUI class created by the Introjucer!

  Be careful when adding custom code to these files, as only the code within
  the "//[xyz]" and "//[/xyz]" sections will be retained when the file is loaded
  and re-saved.

  Created with Introjucer version: 3.1.0

  ------------------------------------------------------------------------------

  The Introjucer is part of the JUCE library - "Jules' Utility Class Extensions"
  Copyright 2004-13 by Raw Material Software Ltd.

  ==============================================================================
*/

//[Headers] You can add your own extra header files here...
//[/Headers]

#include "PluginEditor.h"


//[MiscUserDefs] You can add your own user definitions and misc code here...
//[/MiscUserDefs]

//==============================================================================
Project3AudioProcessorEditor::Project3AudioProcessorEditor (Project3AudioProcessor* ownerFilter)
    : AudioProcessorEditor(ownerFilter)
{
    addAndMakeVisible (slider = new Slider ("new slider"));
    slider->setRange (0, 10, 0);
    slider->setSliderStyle (Slider::RotaryVerticalDrag);
    slider->setTextBoxStyle (Slider::TextBoxBelow, false, 80, 20);
    slider->setColour (Slider::rotarySliderFillColourId, Colour (0x7fffffff));
    slider->setColour (Slider::rotarySliderOutlineColourId, Colour (0x66ffffff));
    slider->setColour (Slider::textBoxTextColourId, Colours::white);
    slider->setColour (Slider::textBoxBackgroundColourId, Colour (0x00ffffff));
    slider->setColour (Slider::textBoxHighlightColourId, Colour (0x001111ee));
    slider->setColour (Slider::textBoxOutlineColourId, Colour (0x00808080));
    slider->addListener (this);

    addAndMakeVisible (slider2 = new Slider ("new slider"));
    slider2->setRange (0, 10000, 0);
    slider2->setSliderStyle (Slider::RotaryVerticalDrag);
    slider2->setTextBoxStyle (Slider::TextBoxBelow, false, 80, 20);
    slider2->setColour (Slider::rotarySliderFillColourId, Colour (0x7fffffff));
    slider2->setColour (Slider::rotarySliderOutlineColourId, Colour (0x66ffffff));
    slider2->setColour (Slider::textBoxTextColourId, Colour (0xffcbcbcb));
    slider2->setColour (Slider::textBoxBackgroundColourId, Colour (0x00ffffff));
    slider2->setColour (Slider::textBoxHighlightColourId, Colour (0x001111ee));
    slider2->setColour (Slider::textBoxOutlineColourId, Colour (0x00808080));
    slider2->addListener (this);

    addAndMakeVisible (slider4 = new Slider ("new slider"));
    slider4->setRange (0, 10, 0);
    slider4->setSliderStyle (Slider::RotaryVerticalDrag);
    slider4->setTextBoxStyle (Slider::TextBoxBelow, false, 80, 20);
    slider4->setColour (Slider::rotarySliderFillColourId, Colour (0x7fffffff));
    slider4->setColour (Slider::rotarySliderOutlineColourId, Colour (0x66ffffff));
    slider4->setColour (Slider::textBoxTextColourId, Colours::white);
    slider4->setColour (Slider::textBoxBackgroundColourId, Colour (0x00ffffff));
    slider4->setColour (Slider::textBoxHighlightColourId, Colour (0x001111ee));
    slider4->setColour (Slider::textBoxOutlineColourId, Colour (0x00808080));
    slider4->addListener (this);

    addAndMakeVisible (label = new Label ("new label",
                                          TRANS("Freq")));
    label->setFont (Font (15.00f, Font::plain));
    label->setJustificationType (Justification::centredLeft);
    label->setEditable (false, false, false);
    label->setColour (Label::textColourId, Colours::white);
    label->setColour (TextEditor::textColourId, Colours::black);
    label->setColour (TextEditor::backgroundColourId, Colour (0x00000000));

    addAndMakeVisible (label2 = new Label ("new label",
                                           TRANS("Pre-Distortion\n")));
    label2->setFont (Font (15.00f, Font::plain));
    label2->setJustificationType (Justification::centredLeft);
    label2->setEditable (false, false, false);
    label2->setColour (Label::textColourId, Colours::white);
    label2->setColour (TextEditor::textColourId, Colours::black);
    label2->setColour (TextEditor::backgroundColourId, Colour (0x00000000));

    addAndMakeVisible (label3 = new Label ("new label",
                                           TRANS("Post-Distortion\n")));
    label3->setFont (Font (15.00f, Font::plain));
    label3->setJustificationType (Justification::centredLeft);
    label3->setEditable (false, false, false);
    label3->setColour (Label::textColourId, Colours::white);
    label3->setColour (TextEditor::textColourId, Colours::black);
    label3->setColour (TextEditor::backgroundColourId, Colour (0x00000000));


    //[UserPreSize]
    //[/UserPreSize]

    setSize (400, 200);


    //[Constructor] You can add your own custom stuff here..
	getProcessor()->RequestUIUpdate(); //Flag for UI update when initialized
	startTimer(200); //200 ms UI updating
    //[/Constructor]
}

Project3AudioProcessorEditor::~Project3AudioProcessorEditor()
{
    //[Destructor_pre]. You can add your own custom destruction code here..
    //[/Destructor_pre]

    slider = nullptr;
    slider2 = nullptr;
    slider4 = nullptr;
    label = nullptr;
    label2 = nullptr;
    label3 = nullptr;


    //[Destructor]. You can add your own custom destruction code here..
    //[/Destructor]
}

//==============================================================================
void Project3AudioProcessorEditor::paint (Graphics& g)
{
    //[UserPrePaint] Add your own custom painting code here..
    //[/UserPrePaint]

    g.fillAll (Colour (0xff01000e));

    g.setColour (Colour (0xff00203f));
    g.fillRect (123, -8, 5, 211);

    g.setColour (Colour (0xff00203f));
    g.fillRect (275, -9, 5, 211);

    //[UserPaint] Add your own custom painting code here..
    //[/UserPaint]
}

void Project3AudioProcessorEditor::resized()
{
    slider->setBounds (24, 80, 72, 80);
    slider2->setBounds (160, 80, 72, 80);
    slider4->setBounds (304, 80, 72, 80);
    label->setBounds (176, 48, 40, 24);
    label2->setBounds (16, 48, 104, 24);
    label3->setBounds (288, 48, 104, 24);
    //[UserResized] Add your own custom resize handling here..
    //[/UserResized]
}

void Project3AudioProcessorEditor::sliderValueChanged (Slider* sliderThatWasMoved)
{
    //[UsersliderValueChanged_Pre]
	Project3AudioProcessor* processor = getProcessor();
    //[/UsersliderValueChanged_Pre]

    if (sliderThatWasMoved == slider)
    {
        //[UserSliderCode_slider] -- add your slider handling code here..
		processor->setParameter(Project3AudioProcessor::preDis, slider->getValue());
        //[/UserSliderCode_slider]
    }
    else if (sliderThatWasMoved == slider2)
    {
        //[UserSliderCode_slider2] -- add your slider handling code here..
		processor->setParameter(Project3AudioProcessor::frequency, slider2->getValue());
        //[/UserSliderCode_slider2]
    }
    else if (sliderThatWasMoved == slider4)
    {
        //[UserSliderCode_slider4] -- add your slider handling code here..
		processor->setParameter(Project3AudioProcessor::postDis, slider4->getValue());
        //[/UserSliderCode_slider4]
    }

    //[UsersliderValueChanged_Post]
    //[/UsersliderValueChanged_Post]
}



//[MiscUserCode] You can add your own definitions of your custom methods or any other code here...
void Project3AudioProcessorEditor::timerCallback()
{
	Project3AudioProcessor* ourProcessor = getProcessor();
	if (ourProcessor->NeedsUIUpdate()) { //Update UI as necessary
		slider->setValue(ourProcessor->getParameter(Project3AudioProcessor::preDis));
		slider2->setValue(ourProcessor->getParameter(Project3AudioProcessor::frequency));
		slider4->setValue(ourProcessor->getParameter(Project3AudioProcessor::postDis));
		ourProcessor->ClearUIUpdateFlag();
	}
}
//[/MiscUserCode]


//==============================================================================
#if 0
/*  -- Introjucer information section --

    This is where the Introjucer stores the metadata that describe this GUI layout, so
    make changes in here at your peril!

BEGIN_JUCER_METADATA

<JUCER_COMPONENT documentType="Component" className="Project3AudioProcessorEditor"
                 componentName="" parentClasses="public AudioProcessorEditor, public Timer"
                 constructorParams="Project3AudioProcessor* ownerFilter" variableInitialisers="AudioProcessorEditor(ownerFilter)"
                 snapPixels="8" snapActive="1" snapShown="1" overlayOpacity="0.330"
                 fixedSize="1" initialWidth="400" initialHeight="200">
  <BACKGROUND backgroundColour="ff01000e">
    <RECT pos="123 -8 5 211" fill="solid: ff00203f" hasStroke="0"/>
    <RECT pos="275 -9 5 211" fill="solid: ff00203f" hasStroke="0"/>
  </BACKGROUND>
  <SLIDER name="new slider" id="580d19dd747f9557" memberName="slider" virtualName=""
          explicitFocusOrder="0" pos="24 80 72 80" rotarysliderfill="7fffffff"
          rotaryslideroutline="66ffffff" textboxtext="ffffffff" textboxbkgd="ffffff"
          textboxhighlight="1111ee" textboxoutline="808080" min="0" max="10"
          int="0" style="RotaryVerticalDrag" textBoxPos="TextBoxBelow"
          textBoxEditable="1" textBoxWidth="80" textBoxHeight="20" skewFactor="1"/>
  <SLIDER name="new slider" id="619b2561b087daaf" memberName="slider2"
          virtualName="" explicitFocusOrder="0" pos="160 80 72 80" rotarysliderfill="7fffffff"
          rotaryslideroutline="66ffffff" textboxtext="ffcbcbcb" textboxbkgd="ffffff"
          textboxhighlight="1111ee" textboxoutline="808080" min="0" max="10000"
          int="0" style="RotaryVerticalDrag" textBoxPos="TextBoxBelow"
          textBoxEditable="1" textBoxWidth="80" textBoxHeight="20" skewFactor="1"/>
  <SLIDER name="new slider" id="4530bf32f8b60d3a" memberName="slider4"
          virtualName="" explicitFocusOrder="0" pos="304 80 72 80" rotarysliderfill="7fffffff"
          rotaryslideroutline="66ffffff" textboxtext="ffffffff" textboxbkgd="ffffff"
          textboxhighlight="1111ee" textboxoutline="808080" min="0" max="10"
          int="0" style="RotaryVerticalDrag" textBoxPos="TextBoxBelow"
          textBoxEditable="1" textBoxWidth="80" textBoxHeight="20" skewFactor="1"/>
  <LABEL name="new label" id="a7dcaf0cf1e76ec2" memberName="label" virtualName=""
         explicitFocusOrder="0" pos="176 48 40 24" textCol="ffffffff"
         edTextCol="ff000000" edBkgCol="0" labelText="Freq" editableSingleClick="0"
         editableDoubleClick="0" focusDiscardsChanges="0" fontname="Default font"
         fontsize="15" bold="0" italic="0" justification="33"/>
  <LABEL name="new label" id="ff88507e75168bd2" memberName="label2" virtualName=""
         explicitFocusOrder="0" pos="16 48 104 24" textCol="ffffffff"
         edTextCol="ff000000" edBkgCol="0" labelText="Pre-Distortion&#10;"
         editableSingleClick="0" editableDoubleClick="0" focusDiscardsChanges="0"
         fontname="Default font" fontsize="15" bold="0" italic="0" justification="33"/>
  <LABEL name="new label" id="8472e01be3ea09d0" memberName="label3" virtualName=""
         explicitFocusOrder="0" pos="288 48 104 24" textCol="ffffffff"
         edTextCol="ff000000" edBkgCol="0" labelText="Post-Distortion&#10;"
         editableSingleClick="0" editableDoubleClick="0" focusDiscardsChanges="0"
         fontname="Default font" fontsize="15" bold="0" italic="0" justification="33"/>
</JUCER_COMPONENT>

END_JUCER_METADATA
*/
#endif


//[EndFile] You can add extra defines here...
//[/EndFile]
