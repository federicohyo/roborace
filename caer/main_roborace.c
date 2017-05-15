/*
 * main.c
 *
 *  Created on: May, 2017
 *      Author: federico.corradi@inilabs.com
 *
 *	Roborace Setup - 4 stereo pairs -
 */

#include "main.h"
#include "base/config.h"
#include "base/config_server.h"
#include "base/log.h"
#include "base/mainloop.h"
#include "base/misc.h"

// Devices support.
#include "modules/ini/davis_fx2.h"
#include "modules/ini/davis_fx3.h"


// Input/Output support.
#ifdef ENABLE_FILE_INPUT
#include "modules/misc/in/file.h"
#endif
#ifdef ENABLE_NETWORK_INPUT
#include "modules/misc/in/net_tcp.h"
#include "modules/misc/in/unix_socket.h"
#endif

#ifdef ENABLE_FILE_OUTPUT
#include "modules/misc/out/file.h"
#endif
#ifdef ENABLE_NETWORK_OUTPUT
#include "modules/misc/out/net_tcp_server.h"
#include "modules/misc/out/net_tcp.h"
#include "modules/misc/out/net_udp.h"
#include "modules/misc/out/unix_socket_server.h"
#include "modules/misc/out/unix_socket.h"
#endif

// Common filters support.
#ifdef ENABLE_BAFILTER
#include "modules/backgroundactivityfilter/backgroundactivityfilter.h"
#endif
#ifdef ENABLE_CAMERACALIBRATION
#include "modules/cameracalibration/cameracalibration.h"
#endif
#ifdef ENABLE_FRAMEENHANCER
#include "modules/frameenhancer/frameenhancer.h"
#endif
#ifdef ENABLE_STATISTICS
#include "modules/statistics/statistics.h"
#endif
#ifdef ENABLE_VISUALIZER
#include "modules/visualizer/visualizer.h"
#endif
#ifdef ENABLE_STEREOCALIBRATION
#include "modules/stereocalibration/stereocalibration.h"
#endif
#ifdef ENABLE_SPIKEFEATURES
#include "modules/spikefeatures/spikefeatures.h"
#endif

static bool mainloop_roborace(void);

static bool mainloop_roborace(void) {
	// An eventPacketContainer bundles event packets of different types together,
	// to maintain time-coherence between the different events.

#ifdef ENABLE_VISUALIZER
	caerVisualizerEventHandler visualizerEventHandler = NULL;
#endif

	caerEventPacketContainer container_cam0 = NULL;
	caerSpecialEventPacket special_cam0 = NULL;
	caerPolarityEventPacket polarity_cam0 = NULL;
	caerFrameEventPacket frame_cam0 = NULL;
	caerIMU6EventPacket imu_cam0 = NULL;

	caerEventPacketContainer container_cam1 = NULL;
	caerSpecialEventPacket special_cam1 = NULL;
	caerPolarityEventPacket polarity_cam1 = NULL;
	caerFrameEventPacket frame_cam1 = NULL;
	caerIMU6EventPacket imu_cam1 = NULL;

	caerEventPacketContainer container_cam2 = NULL;
	caerSpecialEventPacket special_cam2 = NULL;
	caerPolarityEventPacket polarity_cam2 = NULL;
	caerFrameEventPacket frame_cam2 = NULL;
	caerIMU6EventPacket imu_cam2 = NULL;

	caerEventPacketContainer container_cam3 = NULL;
	caerSpecialEventPacket special_cam3 = NULL;
	caerPolarityEventPacket polarity_cam3 = NULL;
	caerFrameEventPacket frame_cam3 = NULL;
	caerIMU6EventPacket imu_cam3 = NULL;

	caerEventPacketContainer container_cam4 = NULL;
	caerSpecialEventPacket special_cam4 = NULL;
	caerPolarityEventPacket polarity_cam4 = NULL;
	caerFrameEventPacket frame_cam4 = NULL;
	caerIMU6EventPacket imu_cam4 = NULL;

	caerEventPacketContainer container_cam5 = NULL;
	caerSpecialEventPacket special_cam5 = NULL;
	caerPolarityEventPacket polarity_cam5 = NULL;
	caerFrameEventPacket frame_cam5 = NULL;
	caerIMU6EventPacket imu_cam5 = NULL;

	caerEventPacketContainer container_cam6 = NULL;
	caerSpecialEventPacket special_cam6 = NULL;
	caerPolarityEventPacket polarity_cam6 = NULL;
	caerFrameEventPacket frame_cam6 = NULL;
	caerIMU6EventPacket imu_cam6 = NULL;

	caerEventPacketContainer container_cam7 = NULL;
	caerSpecialEventPacket special_cam7 = NULL;
	caerPolarityEventPacket polarity_cam7 = NULL;
	caerFrameEventPacket frame_cam7 = NULL;
	caerIMU6EventPacket imu_cam7 = NULL;


#ifdef ENABLE_FILE_INPUT
// Front stereo pair
	// Input modules grab data from outside sources (like devices, files, ...)
	// and put events into an event packet.
	container_cam0 = caerInputFile(1);

	// Typed EventPackets contain events of a certain type.
	special_cam0 = (caerSpecialEventPacket) caerEventPacketContainerGetEventPacket(container_cam0, SPECIAL_EVENT);
	polarity_cam0 = (caerPolarityEventPacket) caerEventPacketContainerGetEventPacket(container_cam0, POLARITY_EVENT);
	frame_cam0 = (caerFrameEventPacket) caerEventPacketContainerGetEventPacket(container_cam0, FRAME_EVENT);
	imu_cam0 = (caerIMU6EventPacket) caerEventPacketContainerGetEventPacket(container_cam0, IMU6_EVENT);

	// Input modules grab data from outside sources (like devices, files, ...)
	// and put events into an event packet.
	container_cam1 = caerInputFile(2);

	// Typed EventPackets contain events of a certain type.
	special_cam1 = (caerSpecialEventPacket) caerEventPacketContainerGetEventPacket(container_cam1, SPECIAL_EVENT);
	polarity_cam1 = (caerPolarityEventPacket) caerEventPacketContainerGetEventPacket(container_cam1, POLARITY_EVENT);
	frame_cam1 = (caerFrameEventPacket) caerEventPacketContainerGetEventPacket(container_cam1, FRAME_EVENT);
	imu_cam1 = (caerIMU6EventPacket) caerEventPacketContainerGetEventPacket(container_cam1, IMU6_EVENT);

// Right Stereo Pair

	// Input modules grab data from outside sources (like devices, files, ...)
	// and put events into an event packet.
	container_cam2 = caerInputFile(3);

	// Typed EventPackets contain events of a certain type.
	special_cam2 = (caerSpecialEventPacket) caerEventPacketContainerGetEventPacket(container_cam2, SPECIAL_EVENT);
	polarity_cam2 = (caerPolarityEventPacket) caerEventPacketContainerGetEventPacket(container_cam2, POLARITY_EVENT);
	frame_cam2 = (caerFrameEventPacket) caerEventPacketContainerGetEventPacket(container_cam2, FRAME_EVENT);
	imu_cam2 = (caerIMU6EventPacket) caerEventPacketContainerGetEventPacket(container_cam2, IMU6_EVENT);

	// Input modules grab data from outside sources (like devices, files, ...)
	// and put events into an event packet.
	container_cam3 = caerInputFile(4);

	// Typed EventPackets contain events of a certain type.
	special_cam3 = (caerSpecialEventPacket) caerEventPacketContainerGetEventPacket(container_cam3, SPECIAL_EVENT);
	polarity_cam3 = (caerPolarityEventPacket) caerEventPacketContainerGetEventPacket(container_cam3, POLARITY_EVENT);
	frame_cam3 = (caerFrameEventPacket) caerEventPacketContainerGetEventPacket(container_cam3, FRAME_EVENT);
	imu_cam3 = (caerIMU6EventPacket) caerEventPacketContainerGetEventPacket(container_cam3, IMU6_EVENT);


// Rear stereo pair

	container_cam4 = caerInputFile(5);

	// Typed EventPackets contain events of a certain type.
	// We search for them by type here, because input modules may not have all or any of them.
	special_cam4 = (caerSpecialEventPacket) caerEventPacketContainerGetEventPacket(container_cam4, SPECIAL_EVENT);
	polarity_cam4 = (caerPolarityEventPacket) caerEventPacketContainerGetEventPacket(container_cam4, POLARITY_EVENT);
	frame_cam4 = (caerFrameEventPacket) caerEventPacketContainerGetEventPacket(container_cam4, FRAME_EVENT);
	imu_cam4 = (caerIMU6EventPacket) caerEventPacketContainerGetEventPacket(container_cam4, IMU6_EVENT);

	container_cam5 = caerInputFile(6);

	// Typed EventPackets contain events of a certain type.
	// We search for them by type here, because input modules may not have all or any of them.
	special_cam5 = (caerSpecialEventPacket) caerEventPacketContainerGetEventPacket(container_cam5, SPECIAL_EVENT);
	polarity_cam5 = (caerPolarityEventPacket) caerEventPacketContainerGetEventPacket(container_cam5, POLARITY_EVENT);
	frame_cam5 = (caerFrameEventPacket) caerEventPacketContainerGetEventPacket(container_cam5, FRAME_EVENT);
	imu_cam5 = (caerIMU6EventPacket) caerEventPacketContainerGetEventPacket(container_cam5, IMU6_EVENT);


// Left stereo pair

	container_cam6 = caerInputFile(7);

	// Typed EventPackets contain events of a certain type.
	// We search for them by type here, because input modules may not have all or any of them.
	special_cam6 = (caerSpecialEventPacket) caerEventPacketContainerGetEventPacket(container_cam6, SPECIAL_EVENT);
	polarity_cam6 = (caerPolarityEventPacket) caerEventPacketContainerGetEventPacket(container_cam6, POLARITY_EVENT);
	frame_cam6 = (caerFrameEventPacket) caerEventPacketContainerGetEventPacket(container_cam6, FRAME_EVENT);
	imu_cam6 = (caerIMU6EventPacket) caerEventPacketContainerGetEventPacket(container_cam6, IMU6_EVENT);

	container_cam7 = caerInputFile(8);

	// Typed EventPackets contain events of a certain type.
	// We search for them by type here, because input modules may not have all or any of them.
	special_cam7 = (caerSpecialEventPacket) caerEventPacketContainerGetEventPacket(container_cam7, SPECIAL_EVENT);
	polarity_cam7 = (caerPolarityEventPacket) caerEventPacketContainerGetEventPacket(container_cam7, POLARITY_EVENT);
	frame_cam7 = (caerFrameEventPacket) caerEventPacketContainerGetEventPacket(container_cam7, FRAME_EVENT);
	imu_cam7 = (caerIMU6EventPacket) caerEventPacketContainerGetEventPacket(container_cam7, IMU6_EVENT);

#endif


	// Filters process event packets: for example to suppress certain events,
	// like with the Background Activity Filter, which suppresses events that
	// look to be uncorrelated with real scene changes (noise reduction).
#ifdef ENABLE_BAFILTER
	caerBackgroundActivityFilter(9, polarity_cam0);
	caerBackgroundActivityFilter(10,polarity_cam1);
	caerBackgroundActivityFilter(11,polarity_cam2);
	caerBackgroundActivityFilter(12,polarity_cam3);
	caerBackgroundActivityFilter(13,polarity_cam4);
	caerBackgroundActivityFilter(14,polarity_cam5);
	caerBackgroundActivityFilter(15,polarity_cam6);
	caerBackgroundActivityFilter(16,polarity_cam7);	
#endif

#ifdef ENABLE_SPIKEFEATURES
	caerFrameEventPacket alpha_cam0 = NULL;;
	caerFrameEventPacket alpha_cam1 = NULL;;
	caerFrameEventPacket alpha_cam2 = NULL;;
	caerFrameEventPacket alpha_cam3 = NULL;;
	caerFrameEventPacket alpha_cam4 = NULL;;
	caerFrameEventPacket alpha_cam5 = NULL;;
	caerFrameEventPacket alpha_cam6 = NULL;;
	caerFrameEventPacket alpha_cam7 = NULL;;
	caerSpikeFeatures(33, polarity_cam0, &alpha_cam0);
	caerSpikeFeatures(34, polarity_cam1, &alpha_cam1);
	caerSpikeFeatures(35, polarity_cam2, &alpha_cam2);
	caerSpikeFeatures(36, polarity_cam3, &alpha_cam3);
	caerSpikeFeatures(37, polarity_cam4, &alpha_cam4);
	caerSpikeFeatures(38, polarity_cam5, &alpha_cam5);
	caerSpikeFeatures(39, polarity_cam6, &alpha_cam6);
	caerSpikeFeatures(40, polarity_cam7, &alpha_cam7);
#endif

	// A simple visualizer exists to show what the output looks like.
#ifdef ENABLE_VISUALIZER
	caerVisualizer(17, "Frame", &caerVisualizerRendererFrameEvents, visualizerEventHandler, (caerEventPacketHeader) frame_cam0);
	caerVisualizer(18, "Frame", &caerVisualizerRendererFrameEvents, visualizerEventHandler, (caerEventPacketHeader) frame_cam1);
	caerVisualizer(19, "Frame", &caerVisualizerRendererFrameEvents, visualizerEventHandler, (caerEventPacketHeader) frame_cam2);
	caerVisualizer(20, "Frame", &caerVisualizerRendererFrameEvents, visualizerEventHandler, (caerEventPacketHeader) frame_cam3);
	caerVisualizer(21, "Frame", &caerVisualizerRendererFrameEvents, visualizerEventHandler, (caerEventPacketHeader) frame_cam4);
	caerVisualizer(22, "Frame", &caerVisualizerRendererFrameEvents, visualizerEventHandler, (caerEventPacketHeader) frame_cam5);
	caerVisualizer(23, "Frame", &caerVisualizerRendererFrameEvents, visualizerEventHandler, (caerEventPacketHeader) frame_cam6);
	caerVisualizer(24, "Frame", &caerVisualizerRendererFrameEvents, visualizerEventHandler, (caerEventPacketHeader) frame_cam7);


	caerVisualizer(25, "Polarity", &caerVisualizerRendererPolarityEvents, visualizerEventHandler, (caerEventPacketHeader) polarity_cam0);
	caerVisualizer(26, "Polarity", &caerVisualizerRendererPolarityEvents, visualizerEventHandler, (caerEventPacketHeader) polarity_cam1);
	caerVisualizer(27, "Polarity", &caerVisualizerRendererPolarityEvents, visualizerEventHandler, (caerEventPacketHeader) polarity_cam2);
	caerVisualizer(28, "Polarity", &caerVisualizerRendererPolarityEvents, visualizerEventHandler, (caerEventPacketHeader) polarity_cam3);
	caerVisualizer(29, "Polarity", &caerVisualizerRendererPolarityEvents, visualizerEventHandler, (caerEventPacketHeader) polarity_cam4);
	caerVisualizer(30, "Polarity", &caerVisualizerRendererPolarityEvents, visualizerEventHandler, (caerEventPacketHeader) polarity_cam5);
	caerVisualizer(31, "Polarity", &caerVisualizerRendererPolarityEvents, visualizerEventHandler, (caerEventPacketHeader) polarity_cam6);
	caerVisualizer(32, "Polarity", &caerVisualizerRendererPolarityEvents, visualizerEventHandler, (caerEventPacketHeader) polarity_cam7);

#ifdef ENABLE_SPIKEFEATURES
	caerVisualizer(41, "Frame", &caerVisualizerRendererFrameEvents, NULL, (caerEventPacketHeader) alpha_cam0);
	caerVisualizer(42, "Frame", &caerVisualizerRendererFrameEvents, NULL, (caerEventPacketHeader) alpha_cam1);
	caerVisualizer(43, "Frame", &caerVisualizerRendererFrameEvents, NULL, (caerEventPacketHeader) alpha_cam2);
	caerVisualizer(44, "Frame", &caerVisualizerRendererFrameEvents, NULL, (caerEventPacketHeader) alpha_cam3);
	caerVisualizer(45, "Frame", &caerVisualizerRendererFrameEvents, NULL, (caerEventPacketHeader) alpha_cam4);
	caerVisualizer(46, "Frame", &caerVisualizerRendererFrameEvents, NULL, (caerEventPacketHeader) alpha_cam5);
	caerVisualizer(47, "Frame", &caerVisualizerRendererFrameEvents, NULL, (caerEventPacketHeader) alpha_cam6);
	caerVisualizer(48, "Frame", &caerVisualizerRendererFrameEvents, NULL, (caerEventPacketHeader) alpha_cam7);
#endif

#endif


	return (true); // If false is returned, processing of this loop stops.
}

int main(int argc, char **argv) {
	// Initialize config storage from file, support command-line overrides.
	// If no init from file needed, pass NULL.
	caerConfigInit("caer-config.xml", argc, argv);

	// Initialize logging sub-system.
	caerLogInit();

	// Initialize visualizer framework (load fonts etc.).
#ifdef ENABLE_VISUALIZER
	caerVisualizerSystemInit();
#endif

	// Daemonize the application (run in background).
	//caerDaemonize();

	// Start the configuration server thread for run-time config changes.
	caerConfigServerStart();

	// Finally run the main event processing loops.
	struct caer_mainloop_definition mainLoops[1] = { { 1, &mainloop_roborace } };
	caerMainloopRun(&mainLoops, 1);

	// After shutting down the mainloops, also shutdown the config server
	// thread if needed.
	caerConfigServerStop();

	return (EXIT_SUCCESS);
}
