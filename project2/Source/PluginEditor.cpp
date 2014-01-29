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
Project2AudioProcessorEditor::Project2AudioProcessorEditor (Project2AudioProcessor* ownerFilter)
    : AudioProcessorEditor(ownerFilter)
{
    addAndMakeVisible (toggleButton = new ToggleButton ("squareToggle"));
    toggleButton->setButtonText (TRANS("Square"));
    toggleButton->setRadioGroupId (1);
    toggleButton->addListener (this);
    toggleButton->setToggleState (true, dontSendNotification);

    addAndMakeVisible (toggleButton2 = new ToggleButton ("new toggle button"));
    toggleButton2->setButtonText (TRANS("Sine"));
    toggleButton2->setRadioGroupId (1);
    toggleButton2->addListener (this);

    addAndMakeVisible (comboBox = new ComboBox ("new combo box"));
    comboBox->setEditableText (false);
    comboBox->setJustificationType (Justification::centredLeft);
    comboBox->setTextWhenNothingSelected (TRANS("50%"));
    comboBox->setTextWhenNoChoicesAvailable (TRANS("(no choices)"));
    comboBox->addItem (TRANS("12.5%"), 1);
    comboBox->addItem (TRANS("25%"), 2);
    comboBox->addItem (TRANS("50%"), 3);
    comboBox->addItem (TRANS("75%"), 4);
    comboBox->addListener (this);

    addAndMakeVisible (label = new Label ("new label",
                                          TRANS("PWM")));
    label->setFont (Font (15.00f, Font::plain));
    label->setJustificationType (Justification::centredLeft);
    label->setEditable (false, false, false);
    label->setColour (TextEditor::textColourId, Colours::black);
    label->setColour (TextEditor::backgroundColourId, Colour (0x00000000));

    addAndMakeVisible (toggleButton3 = new ToggleButton ("new toggle button"));
    toggleButton3->setButtonText (TRANS("Noise"));
    toggleButton3->setRadioGroupId (1);
    toggleButton3->addListener (this);


    //[UserPreSize]
    //[/UserPreSize]

    setSize (200, 175);


    //[Constructor] You can add your own custom stuff here..
	startTimer(200);
    //[/Constructor]
}

Project2AudioProcessorEditor::~Project2AudioProcessorEditor()
{
    //[Destructor_pre]. You can add your own custom destruction code here..
    //[/Destructor_pre]

    toggleButton = nullptr;
    toggleButton2 = nullptr;
    comboBox = nullptr;
    label = nullptr;
    toggleButton3 = nullptr;


    //[Destructor]. You can add your own custom destruction code here..
    //[/Destructor]
}

//==============================================================================
void Project2AudioProcessorEditor::paint (Graphics& g)
{
    //[UserPrePaint] Add your own custom painting code here..
    //[/UserPrePaint]

    g.fillAll (Colour (0xfffdf7c5));

    g.setColour (Colour (0xff09c0bb));
    g.fillRect (-9, 63, 216, 4);

    g.setColour (Colour (0xff09c0bb));
    g.fillRect (-1, 119, 216, 4);

    //[UserPaint] Add your own custom painting code here..
    //[/UserPaint]
}

void Project2AudioProcessorEditor::resized()
{
    toggleButton->setBounds (8, 8, 80, 24);
    toggleButton2->setBounds (8, 80, 72, 24);
    comboBox->setBounds (104, 32, 78, 24);
    label->setBounds (104, 8, 40, 24);
    toggleButton3->setBounds (8, 136, 72, 24);
    //[UserResized] Add your own custom resize handling here..
    //[/UserResized]
}

void Project2AudioProcessorEditor::buttonClicked (Button* buttonThatWasClicked)
{
    //[UserbuttonClicked_Pre]
	Project2AudioProcessor* ourProcessor = getProcessor();
    //[/UserbuttonClicked_Pre]

    if (buttonThatWasClicked == toggleButton)
    {
        //[UserButtonCode_toggleButton] -- add your button handler code here..
		switch (comboBox->getSelectedItemIndex()){
		case 0:
			ourProcessor->setParameter(Project2AudioProcessor::Square12, 1);
			break;
		case 1:
			ourProcessor->setParameter(Project2AudioProcessor::Square25, 1);
			break;
		case 2:
			ourProcessor->setParameter(Project2AudioProcessor::Square50, 1);
			break;
		case 3:
			ourProcessor->setParameter(Project2AudioProcessor::Square75, 1);
			break;
		default:
			ourProcessor->setParameter(Project2AudioProcessor::Square50, 1);
			break;
		}
        //[/UserButtonCode_toggleButton]
    }
    else if (buttonThatWasClicked == toggleButton2)
    {
        //[UserButtonCode_toggleButton2] -- add your button handler code here..
		ourProcessor->setParameter(Project2AudioProcessor::sine, 1);
        //[/UserButtonCode_toggleButton2]
    }
    else if (buttonThatWasClicked == toggleButton3)
    {
        //[UserButtonCode_toggleButton3] -- add your button handler code here..
		ourProcessor->setParameter(Project2AudioProcessor::noise, 1);
        //[/UserButtonCode_toggleButton3]
    }

    //[UserbuttonClicked_Post]
    //[/UserbuttonClicked_Post]
}

void Project2AudioProcessorEditor::comboBoxChanged (ComboBox* comboBoxThatHasChanged)
{
    //[UsercomboBoxChanged_Pre]
	Project2AudioProcessor* ourProcessor = getProcessor();
    //[/UsercomboBoxChanged_Pre]

    if (comboBoxThatHasChanged == comboBox)
    {
        //[UserComboBoxCode_comboBox] -- add your combo box handling code here..
		switch (comboBox->getSelectedItemIndex()){
		case 0:
			ourProcessor->setParameter(Project2AudioProcessor::Square12, 1);
			break;
		case 1:
			ourProcessor->setParameter(Project2AudioProcessor::Square25, 1);
			break;
		case 2:
			ourProcessor->setParameter(Project2AudioProcessor::Square50, 1);
			break;
		case 3:
			ourProcessor->setParameter(Project2AudioProcessor::Square75, 1);
			break;
		default:
			ourProcessor->setParameter(Project2AudioProcessor::Square50, 1);
			break;
		}
        //[/UserComboBoxCode_comboBox]
    }

    //[UsercomboBoxChanged_Post]
    //[/UsercomboBoxChanged_Post]
}



//[MiscUserCode] You can add your own definitions of your custom methods or any other code here...
void Project2AudioProcessorEditor::timerCallback()
{
}
//[/MiscUserCode]


//==============================================================================
#if 0
/*  -- Introjucer information section --

    This is where the Introjucer stores the metadata that describe this GUI layout, so
    make changes in here at your peril!

BEGIN_JUCER_METADATA

<JUCER_COMPONENT documentType="Component" className="Project2AudioProcessorEditor"
                 componentName="" parentClasses="public AudioProcessorEditor, public Timer"
                 constructorParams="Project2AudioProcessor* ownerFilter" variableInitialisers="AudioProcessorEditor(ownerFilter)"
                 snapPixels="8" snapActive="1" snapShown="1" overlayOpacity="0.330"
                 fixedSize="1" initialWidth="200" initialHeight="175">
  <BACKGROUND backgroundColour="fffdf7c5">
    <RECT pos="-9 63 216 4" fill="solid: ff09c0bb" hasStroke="0"/>
    <RECT pos="-1 119 216 4" fill="solid: ff09c0bb" hasStroke="0"/>
  </BACKGROUND>
  <TOGGLEBUTTON name="squareToggle" id="109f2301be19c538" memberName="toggleButton"
                virtualName="" explicitFocusOrder="0" pos="8 8 80 24" buttonText="Square"
                connectedEdges="0" needsCallback="1" radioGroupId="1" state="1"/>
  <TOGGLEBUTTON name="new toggle button" id="8e252431f0f7c0ee" memberName="toggleButton2"
                virtualName="" explicitFocusOrder="0" pos="8 80 72 24" buttonText="Sine"
                connectedEdges="0" needsCallback="1" radioGroupId="1" state="0"/>
  <COMBOBOX name="new combo box" id="be70909d40c8c25a" memberName="comboBox"
            virtualName="" explicitFocusOrder="0" pos="104 32 78 24" editable="0"
            layout="33" items="12.5%&#10;25%&#10;50%&#10;75%" textWhenNonSelected="50%"
            textWhenNoItems="(no choices)"/>
  <LABEL name="new label" id="bf277468d63dc796" memberName="label" virtualName=""
         explicitFocusOrder="0" pos="104 8 40 24" edTextCol="ff000000"
         edBkgCol="0" labelText="PWM" editableSingleClick="0" editableDoubleClick="0"
         focusDiscardsChanges="0" fontname="Default font" fontsize="15"
         bold="0" italic="0" justification="33"/>
  <TOGGLEBUTTON name="new toggle button" id="ef84658b380d4e" memberName="toggleButton3"
                virtualName="" explicitFocusOrder="0" pos="8 136 72 24" buttonText="Noise"
                connectedEdges="0" needsCallback="1" radioGroupId="1" state="0"/>
</JUCER_COMPONENT>

END_JUCER_METADATA
*/
#endif


//[EndFile] You can add extra defines here...
//[/EndFile]
