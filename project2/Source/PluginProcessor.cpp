/*
  ==============================================================================

    This file was auto-generated!

    It contains the basic startup code for a Juce application.

  ==============================================================================
*/

#include "PluginProcessor.h"
#include "PluginEditor.h"

/* Simple sythesizer base, plays all notes/channels */
class MySynthSound : public SynthesiserSound
{
public:
	MySynthSound() {}

	bool appliesToNote(const int) {
		return true;
	}

	bool appliesToChannel(const int) {
		return true;
	}
}

/* Code for the syth voice processing */
class MySynthVoice : public SynthesiserVoice
{
public:
	MySynthVoice()
	{
	}
}

//==============================================================================
Project2AudioProcessor::Project2AudioProcessor()
{
}

Project2AudioProcessor::~Project2AudioProcessor()
{
}

//==============================================================================
const String Project2AudioProcessor::getName() const
{
    return JucePlugin_Name;
}

int Project2AudioProcessor::getNumParameters()
{
    return 0;
}

float Project2AudioProcessor::getParameter (int index)
{
    return 0.0f;
}

void Project2AudioProcessor::setParameter (int index, float newValue)
{
}

const String Project2AudioProcessor::getParameterName (int index)
{
    return String::empty;
}

const String Project2AudioProcessor::getParameterText (int index)
{
    return String::empty;
}

const String Project2AudioProcessor::getInputChannelName (int channelIndex) const
{
    return String (channelIndex + 1);
}

const String Project2AudioProcessor::getOutputChannelName (int channelIndex) const
{
    return String (channelIndex + 1);
}

bool Project2AudioProcessor::isInputChannelStereoPair (int index) const
{
    return true;
}

bool Project2AudioProcessor::isOutputChannelStereoPair (int index) const
{
    return true;
}

bool Project2AudioProcessor::acceptsMidi() const
{
   #if JucePlugin_WantsMidiInput
    return true;
   #else
    return false;
   #endif
}

bool Project2AudioProcessor::producesMidi() const
{
   #if JucePlugin_ProducesMidiOutput
    return true;
   #else
    return false;
   #endif
}

bool Project2AudioProcessor::silenceInProducesSilenceOut() const
{
    return false;
}

double Project2AudioProcessor::getTailLengthSeconds() const
{
    return 0.0;
}

int Project2AudioProcessor::getNumPrograms()
{
    return 0;
}

int Project2AudioProcessor::getCurrentProgram()
{
    return 0;
}

void Project2AudioProcessor::setCurrentProgram (int index)
{
}

const String Project2AudioProcessor::getProgramName (int index)
{
    return String::empty;
}

void Project2AudioProcessor::changeProgramName (int index, const String& newName)
{
}

//==============================================================================
void Project2AudioProcessor::prepareToPlay (double sampleRate, int samplesPerBlock)
{
    // Use this method as the place to do any pre-playback
    // initialisation that you need..
}

void Project2AudioProcessor::releaseResources()
{
    // When playback stops, you can use this as an opportunity to free up any
    // spare memory, etc.
}

void Project2AudioProcessor::processBlock (AudioSampleBuffer& buffer, MidiBuffer& midiMessages)
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
bool Project2AudioProcessor::hasEditor() const
{
    return true; // (change this to false if you choose to not supply an editor)
}

AudioProcessorEditor* Project2AudioProcessor::createEditor()
{
    return new Project2AudioProcessorEditor (this);
}

//==============================================================================
void Project2AudioProcessor::getStateInformation (MemoryBlock& destData)
{
    // You should use this method to store your parameters in the memory block.
    // You could do that either as raw data, or use the XML or ValueTree classes
    // as intermediaries to make it easy to save and load complex data.
}

void Project2AudioProcessor::setStateInformation (const void* data, int sizeInBytes)
{
    // You should use this method to restore your parameters from this memory block,
    // whose contents will have been created by the getStateInformation() call.
}

//==============================================================================
// This creates new instances of the plugin..
AudioProcessor* JUCE_CALLTYPE createPluginFilter()
{
    return new Project2AudioProcessor();
}
