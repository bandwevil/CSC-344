/*
  ==============================================================================

    This file was auto-generated!

    It contains the basic startup code for a Juce application.

  ==============================================================================
*/

#include "PluginProcessor.h"
#include "PluginEditor.h"


//==============================================================================
Project3AudioProcessor::Project3AudioProcessor()
{
}

Project3AudioProcessor::~Project3AudioProcessor()
{
}

//==============================================================================
const String Project3AudioProcessor::getName() const
{
    return JucePlugin_Name;
}

int Project3AudioProcessor::getNumParameters()
{
    return 0;
}

float Project3AudioProcessor::getParameter (int index)
{
    return 0.0f;
}

void Project3AudioProcessor::setParameter (int index, float newValue)
{
}

const String Project3AudioProcessor::getParameterName (int index)
{
    return String::empty;
}

const String Project3AudioProcessor::getParameterText (int index)
{
    return String::empty;
}

const String Project3AudioProcessor::getInputChannelName (int channelIndex) const
{
    return String (channelIndex + 1);
}

const String Project3AudioProcessor::getOutputChannelName (int channelIndex) const
{
    return String (channelIndex + 1);
}

bool Project3AudioProcessor::isInputChannelStereoPair (int index) const
{
    return true;
}

bool Project3AudioProcessor::isOutputChannelStereoPair (int index) const
{
    return true;
}

bool Project3AudioProcessor::acceptsMidi() const
{
   #if JucePlugin_WantsMidiInput
    return true;
   #else
    return false;
   #endif
}

bool Project3AudioProcessor::producesMidi() const
{
   #if JucePlugin_ProducesMidiOutput
    return true;
   #else
    return false;
   #endif
}

bool Project3AudioProcessor::silenceInProducesSilenceOut() const
{
    return false;
}

double Project3AudioProcessor::getTailLengthSeconds() const
{
    return 0.0;
}

int Project3AudioProcessor::getNumPrograms()
{
    return 0;
}

int Project3AudioProcessor::getCurrentProgram()
{
    return 0;
}

void Project3AudioProcessor::setCurrentProgram (int index)
{
}

const String Project3AudioProcessor::getProgramName (int index)
{
    return String::empty;
}

void Project3AudioProcessor::changeProgramName (int index, const String& newName)
{
}

//==============================================================================
void Project3AudioProcessor::prepareToPlay (double sampleRate, int samplesPerBlock)
{
    // Use this method as the place to do any pre-playback
    // initialisation that you need..
}

void Project3AudioProcessor::releaseResources()
{
    // When playback stops, you can use this as an opportunity to free up any
    // spare memory, etc.
}

void Project3AudioProcessor::processBlock (AudioSampleBuffer& buffer, MidiBuffer& midiMessages)
{
    // This is the place where you'd normally do the guts of your plugin's
    // audio processing...
    for (int channel = 0; channel < getNumInputChannels(); ++channel)
    {
        float* channelData = buffer.getSampleData (channel);

        // ..do something to the data...
    }

    // In case we have more outputs than inputs, we'll clear any output
    // channels that didn't contain input data, (because these aren't
    // guaranteed to be empty - they may contain garbage).
    for (int i = getNumInputChannels(); i < getNumOutputChannels(); ++i)
    {
        buffer.clear (i, 0, buffer.getNumSamples());
    }
}

//==============================================================================
bool Project3AudioProcessor::hasEditor() const
{
    return true; // (change this to false if you choose to not supply an editor)
}

AudioProcessorEditor* Project3AudioProcessor::createEditor()
{
    return new Project3AudioProcessorEditor (this);
}

//==============================================================================
void Project3AudioProcessor::getStateInformation (MemoryBlock& destData)
{
    // You should use this method to store your parameters in the memory block.
    // You could do that either as raw data, or use the XML or ValueTree classes
    // as intermediaries to make it easy to save and load complex data.
}

void Project3AudioProcessor::setStateInformation (const void* data, int sizeInBytes)
{
    // You should use this method to restore your parameters from this memory block,
    // whose contents will have been created by the getStateInformation() call.
}

//==============================================================================
// This creates new instances of the plugin..
AudioProcessor* JUCE_CALLTYPE createPluginFilter()
{
    return new Project3AudioProcessor();
}
